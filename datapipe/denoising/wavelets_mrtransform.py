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
Denoise FITS and PNG images with Wavelet Transform.

This script use mr_transform -- a program written CEA/CosmoStat
(www.cosmostat.org) -- to make Wavelet Transform.

It originally came from
https://github.com/jdhp-sap/snippets/blob/master/mr_transform/mr_transform_wrapper_denoising.py.

Example usages:
  ./denoising_with_wavelets_mr_transform.py -h
  ./denoising_with_wavelets_mr_transform.py ./test.fits
  ipython3 -- ./denoising_with_wavelets_mr_transform.py -n4 ./test.fits

This script requires the mr_transform program
(http://www.cosmostat.org/software/isap/).

It also requires Numpy and Matplotlib Python libraries.
"""

__all__ = ['wavelet_transform']

import argparse
import datetime
import json
import os
import numpy as np
import time

from datapipe.benchmark import assess
from datapipe.io import images


def wavelet_transform(input_img, number_of_scales=4, base_file_path="wavelet", verbose=False):
    """
    Do the wavelet transform.
    """

    input_file_path = base_file_path + "_in.fits"
    mr_output_file_path = base_file_path + "_mr_planes.fits"

    # WRITE THE INPUT FILE (FITS) ##########################

    images.save(input_img, input_file_path)

    # EXECUTE MR_TRANSFORM #################################

    # TODO: improve the following lines
    cmd = 'mr_transform -n{} "{}" {}_out'.format(number_of_scales, input_file_path, base_file_path)
    os.system(cmd)

    # TODO: improve the following lines
    cmd = "mv {}_out.mr {}".format(base_file_path, mr_output_file_path)
    os.system(cmd)

    # READ THE MR_TRANSFORM OUTPUT FILE ####################

    output_imgs = images.load(mr_output_file_path, 0)

    if output_imgs.ndim != 3:
        raise Exception("Unexpected error: the output FITS file should contain a 3D array.")

    # DENOISE THE INPUT IMAGE WITH MR_TRANSFORM PLANES #####

    denoised_img = np.zeros(input_img.shape)

    for img_index, img in enumerate(output_imgs):

        if img_index < (len(output_imgs) - 1):  # All planes except the last one

            # Compute the standard deviation of the plane ##

            img_sigma = np.std(img)

            # Apply a threshold on the plane ###############

            # Remark: "abs(img) > (img_sigma * 3.)" should be the correct way to
            # make the image mask, but sometimes results looks better when all
            # negative coefficients are dropped ("img > (img_sigma * 3.)")

            #img_mask = abs(img) > (img_sigma * 3.)  
            img_mask = img > (img_sigma * 3.)
            cleaned_img = img * img_mask

            if verbose:
                images.mpl_save(img,
                                "{}_wt_plane{}.pdf".format(base_file_path, img_index),
                                title="Plane {}".format(img_index))
                images.mpl_save(img_mask,
                                "{}_wt_plane{}_mask.pdf".format(base_file_path, img_index),
                                title="Binary mask for plane {}".format(img_index))
                images.mpl_save(cleaned_img,
                                "{}_wt_plane{}_filtered.pdf".format(base_file_path, img_index),
                                title="Filtered plane {}".format(img_index))

                images.plot(img, title="Plane {}".format(img_index))
                images.plot(img_mask, title="Binary mask for plane {}".format(img_index))
                images.plot(cleaned_img, title="Filtered plane {}".format(img_index))

            # Sum the plane ################################

            denoised_img = denoised_img + cleaned_img

        else:   # The last plane should be kept unmodified

            if verbose:
                images.mpl_save(img,
                                "{}_wt_plane{}.pdf".format(base_file_path, img_index),
                                title="Plane {}".format(img_index))
                images.plot(img, title="Plane {}".format(img_index))

            # Sum the last plane ###########################

            denoised_img = denoised_img + img
    
    return denoised_img


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
    input_file_or_dir_path_list = args.fileargs

    if benchmark_method is not None:
        file_path_list = []
        score_list = []
        execution_time_list = []

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

            # READ THE INPUT FILE #################################################

            input_img = images.load(input_file_path, hdu_index)

            if input_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


            # WAVELET TRANSFORM WITH MR_TRANSFORM #################################

            base_file_path = os.path.basename(input_file_path)
            base_file_path = os.path.splitext(base_file_path)[0]

            initial_time = time.perf_counter()
            cleaned_img = wavelet_transform(input_img, number_of_scales, base_file_path)
            execution_time = time.perf_counter() - initial_time

            # GET THE REFERENCE IMAGE #############################################

            reference_img = images.load(input_file_path, 1)

            # ASSESS OR PRINT THE CLEANED IMAGE ###################################

            try:
                if benchmark_method is None:
                    image_list = [input_img, reference_img, cleaned_img] 
                    title_list = ["Input image", "Reference image", "Cleaned image"] 
                    output = "{}_wt.pdf".format(base_file_path)

                    images.plot_list(image_list, title_list)
                    images.mpl_save_list(image_list, output, title_list)
                else:
                    score_tuple = assess.assess_image_cleaning(input_img, cleaned_img, reference_img, benchmark_method)

                    file_path_list.append(input_file_path)
                    score_list.append(score_tuple)
                    execution_time_list.append(execution_time)
            except assess.EmptyReferenceImageError:
                print("Empty reference image error")
            except assess.EmptyOutputImageError:
                # TODO: if only the output is zero then this is ackward: this
                #       is an algorithm mistake but it cannot be assessed...
                print("Empty output image error")

    if benchmark_method is not None:
        print(score_list)

        output_dict = {}
        output_dict["algo"] = __file__
        output_dict["label"] = "WT"
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
            #json.dump(data, fd)                                 # no pretty print
            json.dump(output_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == "__main__":
    main()

