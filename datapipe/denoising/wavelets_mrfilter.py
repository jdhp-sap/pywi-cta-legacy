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
import numpy as np
import os
import time

import datapipe.denoising
from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
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

class WaveletTransform(AbstractCleaningAlgorithm):

    def __init__(self):
        super(WaveletTransform, self).__init__()
        self.label = "WT (mr_filter)"  # Name to show in plots

    def clean_image(self,
                    input_img,
                    number_of_scales=4,
                    suppress_last_scale=True,
                    suppress_isolated_pixels=True,
                    coef_detection_method=1,
                    k_sigma_noise_threshold=3,
                    noise_model=3,
                    detect_only_positive_structure=False,
                    suppress_positivity_constraint=False):
        """
        Do the wavelet transform.

        mr_filter
        -K         Suppress the last scale (to have background pixels = 0)
        -k         Suppress isolated pixels in the support
        -F2        First scale used for the detection (smooth the resulting image)
        -C1        Coef_Detection_Method: K-SigmaNoise Threshold
        -s3        K-SigmaNoise Threshold = 3 sigma
        -m2        Noise model (try -m2 or -m10) -> -m10 works better but is much slower...
        -p         Detect only positive structure
        -P         Suppress the positivity constraint

        Raises
        ------
        WrongDimensionError
            If `cleaned_img` is not a 2D array.
        """

        if input_img.ndim != 2:
            raise WrongDimensionError()

        input_file_path = ".tmp_{}_{}_in.fits".format(os.getpid(), time.time())
        mr_output_file_path = ".tmp_{}_{}_out.fits".format(os.getpid(), time.time())

#        # CHANGE THE SCALE #####################################
#        
#        input_img = np.log10(input_img + 10.)

        # WRITE THE INPUT FILE (FITS) ##########################

        try:
            images.save(input_img, input_file_path)
        except:
            print("Error on input FITS file:", input_file_path)
            raise

        # EXECUTE MR_FILTER ####################################

        # TODO: improve the following lines
        cmd = 'mr_filter'
        cmd += ' -n{}'.format(number_of_scales)
        cmd += ' -K' if suppress_last_scale else ''
        cmd += ' -k' if suppress_isolated_pixels else ''
        cmd += ' -C{}'.format(coef_detection_method)
        cmd += ' -s{}'.format(k_sigma_noise_threshold)
        cmd += ' -m{}'.format(noise_model)
        cmd += ' -p' if detect_only_positive_structure else ''
        cmd += ' -P' if suppress_positivity_constraint else ''
        self.label = "WT ({})".format(cmd)  # Name to show in plots

        cmd += ' "{}" {}'.format(input_file_path, mr_output_file_path)

        #cmd = 'mr_filter -K -k -C1 -s3 -m3 -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)
        #cmd = 'mr_filter -K -k -C1 -s3 -m2 -p -P -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)

        if self.verbose:
            print(cmd)

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

        # REMOVE FITS FILES ####################################

        os.remove(input_file_path)
        os.remove(mr_output_file_path)

        # CHECK RESULT #########################################

        if cleaned_img.ndim != 2:
            raise WrongDimensionError()

#        # CHANGE THE SCALE #####################################
#        
#        cleaned_img = np.power(10., cleaned_img) - 10.

        return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="Number of scales used in the multiresolution transform")

    parser.add_argument("--suppress-last-scale", "-K", action="store_true",
                        help="Suppress the last scale (to have background pixels = 0)")

    parser.add_argument("--suppress-isolated-pixels", "-k", action="store_true",
                        help="Suppress isolated pixels in the support")

    parser.add_argument("--coef-detection-method", "-C", type=int, default=1, metavar="INTEGER",
                        help="""Coef_Detection_Method:
                            1: K-SigmaNoise Threshold
                            2: False Discovery Rate (FDR) Theshold
                            3: Universal Threshold
                            4: SURE Threshold
                            5: Multiscale SURE Threshold
                            default is K-SigmaNoise Threshold""")

    parser.add_argument("--k-sigma-noise-threshold", "-s", type=float, default=3, metavar="FLOAT",
                        help="Thresholding at nsigma * SigmaNoise")

    parser.add_argument("--noise-model", "-m", type=int, default=3, metavar="INTEGER",
                        help="""Noise model:
                            1: Gaussian noise
                            2: Poisson noise
                            3: Poisson noise + Gaussian noise
                            4: Multiplicative noise
                            5: Non-stationary additive noise
                            6: Non-stationary multiplicative noise
                            7: Undefined stationary noise
                            8: Undefined noise
                            9: Stationary correlated noise
                            10: Poisson noise with few events""")

    parser.add_argument("--detect-only-positive-structure", "-p", action="store_true",
                        help="Detect only positive structure")

    parser.add_argument("--suppress-positivity-constraint", "-P", action="store_true",
                        help="Suppress positivity constraint")

    # COMMON OPTIONS

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

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

    number_of_scales = args.number_of_scales
    suppress_last_scale = args.suppress_last_scale
    suppress_isolated_pixels = args.suppress_isolated_pixels
    coef_detection_method = args.coef_detection_method
    k_sigma_noise_threshold = args.k_sigma_noise_threshold
    noise_model = args.noise_model
    detect_only_positive_structure = args.detect_only_positive_structure
    suppress_positivity_constraint = args.suppress_positivity_constraint

    benchmark_method = args.benchmark
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {
                "number_of_scales": number_of_scales,
                "suppress_last_scale": suppress_last_scale,
                "suppress_isolated_pixels": suppress_isolated_pixels,
                "coef_detection_method": coef_detection_method,
                "k_sigma_noise_threshold": k_sigma_noise_threshold,
                "noise_model": noise_model,
                "detect_only_positive_structure": detect_only_positive_structure,
                "suppress_positivity_constraint": suppress_positivity_constraint
            }

    cleaning_algorithm = WaveletTransform()
    cleaning_algorithm.run(cleaning_function_params,
                           input_file_or_dir_path_list,
                           benchmark_method,
                           output_file_path,
                           plot,
                           saveplot)


if __name__ == "__main__":
    main()

