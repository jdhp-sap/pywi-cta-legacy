#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Denoise FITS images with Wavelet Transform.

This script use mr_filter -- a program written CEA/CosmoStat
(www.cosmostat.org) -- to make Wavelet Transform.

Example usages:
  ./denoising_with_wavelets_mr_filter.py -h
  ./denoising_with_wavelets_mr_filter.py ./test.fits
  ipython3 -- ./denoising_with_wavelets_mr_filter.py -n4 ./test.fits

This script requires the mr_filter program
(http://www.cosmostat.org/software/isap/).
"""

__all__ = ['wavelet_transform']

import argparse
import datetime
import json
import os
import numpy as np
import sys
import tempfile
import time
import traceback

from datapipe.benchmark import assess
from datapipe.io import images


# EXCEPTIONS #################################################################

class MrFilterError(Exception):
    pass

class WrongDimensionError(MrFilterError):
    """Exception raised when trying to save a FITS with more than 3 dimensions
    or less than 2 dimensions.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        super(WrongDimensionError, self).__init__("Unexpected error: the output FITS file should contain a 2D array.")


##############################################################################

def wavelet_transform(input_img, number_of_scales=4, verbose=False):
    """
    Do the wavelet transform.

    mr_filter
    -K         Suppress the last scale (to have background pixels = 0)
    -k         Suppress isolated pixels in the support
    -F2        First scale used for the detection (smooth the resulting image)
    -C1        Coef_Detection_Method: K-SigmaNoise Threshold
    -s3        K-SigmaNoise Threshold = 3 sigma
    -m2        Noise model (try -m2 or -m10) -> -m10 works better but is much slower...

    eventuellement -w pour le debug
    -p  ?      Detect only positive structure
    -P  ?      Suppress the positivity constraint

    Raises
    ------
    WrongDimensionError
        If `cleaned_img` is not a 2D array.
    """

    if input_img.ndim != 2:
        raise WrongDimensionError()

    # Make a temporary directory to store fits files
    with tempfile.TemporaryDirectory() as temp_dir_path:

        input_file_path = os.path.join(temp_dir_path, "in.fits")
        mr_output_file_path = os.path.join(temp_dir_path, "out.fits")

        # WRITE THE INPUT FILE (FITS) ##########################

        try:
            images.save(input_img, input_file_path)
        except:
            print("Error on input FITS file:", input_file_path)
            raise

        # EXECUTE MR_FILTER ####################################

        # TODO: improve the following lines
        #cmd = 'mr_filter -K -k -C1 -s3 -m2 -p -P -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)
        cmd = 'mr_filter -K -k -C1 -s3 -m3 -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)

        try:
            os.system(cmd)
        except:
            print("Error on command:", cmd)
            raise

        # READ THE MR_FILTER OUTPUT FILE #######################

        try:
            cleaned_img = images.load(mr_output_file_path, 0)
        except:
            print("Error on output FITS file:", mr_output_file_path)
            raise

    # The temporary directory and all its contents are removed now

    if cleaned_img.ndim != 2:
        raise WrongDimensionError()

    return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")

    parser.add_argument("--hdu", "-H", type=int, default=0, metavar="INTEGER", 
                        help="The index of the HDU image to use for FITS input files")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", default=None, metavar="FILE",
                        help="The output file where to save plotted images")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    benchmark_method = args.benchmark
    number_of_scales = args.number_of_scales
    hdu_index = args.hdu
    plot = args.plot
    saveplot = args.saveplot
    input_file_or_dir_path_list = args.fileargs

    if benchmark_method is not None:
        file_path_list = []
        score_list = []
        execution_time_list = []
        error_list = []

    for input_file_or_dir_path in input_file_or_dir_path_list:

        if os.path.isdir(input_file_or_dir_path):
            input_file_path_list = []
            for dir_item in os.listdir(input_file_or_dir_path):
                dir_item_path = os.path.join(input_file_or_dir_path, dir_item)
                if dir_item_path.lower().endswith('.fits') and os.path.isfile(dir_item_path):
                    input_file_path_list.append(dir_item_path)
        else:
            input_file_path_list = [input_file_or_dir_path]

        for input_file_path in input_file_path_list:

            # CLEAN ONE IMAGE #########################################################

            try:
                # READ THE INPUT FILE #################################################

                input_img = images.load(input_file_path, hdu_index)

                # WAVELET TRANSFORM WITH MR_FILTER ####################################

                initial_time = time.perf_counter()
                cleaned_img = wavelet_transform(input_img, number_of_scales)
                execution_time = time.perf_counter() - initial_time

                # GET THE REFERENCE IMAGE #############################################

                reference_img = images.load(input_file_path, hdu_index=1)

                # ASSESS OR PRINT THE CLEANED IMAGE ###################################

                if benchmark_method is not None:
                    score_tuple = assess.assess_image_cleaning(input_img,
                                                               cleaned_img,
                                                               reference_img,
                                                               benchmark_method)

                    file_path_list.append(input_file_path)
                    score_list.append(score_tuple)
                    execution_time_list.append(execution_time)

                # PLOT IMAGES #########################################################

                if plot or (saveplot is not None):
                    image_list = [input_img, reference_img, cleaned_img] 
                    title_list = ["Input image", "Reference image", "Cleaned image"] 

                    if plot:
                        images.plot_list(image_list, title_list)

                    if saveplot is not None:
                        images.mpl_save_list(image_list, saveplot, title_list)

            except Exception as e:
                print("Abort image {}: {} ({})".format(input_file_path, e, type(e)))
                #traceback.print_tb(e.__traceback__, file=sys.stdout)

                if benchmark_method is not None:
                    error_dict = {"file": input_file_path,
                                  "type": str(type(e)),
                                  "message": str(e)}
                    error_list.append(error_dict)

    if benchmark_method is not None:
        print(score_list)
        print("{} images aborted".format(len(error_list)))

        output_dict = {}
        output_dict["algo"] = __file__
        output_dict["label"] = "WT (mr_filter)"
        output_dict["algo_params"] = {"number_of_scales": number_of_scales}
        output_dict["benchmark_method"] = benchmark_method
        output_dict["date_time"] = str(datetime.datetime.now())
        output_dict["hdu_index"] = hdu_index
        output_dict["system"] = " ".join(os.uname())
        output_dict["input_file_path_list"] = file_path_list
        output_dict["score_list"] = score_list
        output_dict["execution_time_list"] = execution_time_list

        if args.output is None:
            output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
        else:
            output_file_path = args.output

        with open(output_file_path, "w") as fd:
            json.dump(output_dict, fd, sort_keys=True, indent=4)  # pretty print format

        with open("errors_" + output_file_path, "w") as fd:
            json.dump(error_list, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == "__main__":
    main()

