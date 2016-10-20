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
                    type_of_multiresolution_transform=None,
                    type_of_filters=None,
                    type_of_non_orthog_filters=None,
                    number_of_scales=None,
                    suppress_last_scale=True,
                    suppress_isolated_pixels=True,
                    coef_detection_method=None,
                    k_sigma_noise_threshold=None,
                    noise_model=None,
                    detect_only_positive_structure=False,
                    suppress_positivity_constraint=False,
                    type_of_filtering=None,
                    first_detection_scale=None,
                    number_of_iterations=None,
                    epsilon=None,
                    support_file_name=None,
                    precision=None,
                    verbose=False):
        """
        Do the wavelet transform.

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
        cmd += ' -t{}'.format(type_of_multiresolution_transform) if type_of_multiresolution_transform is not None else ''
        cmd += ' -T{}'.format(type_of_filters) if type_of_filters is not None else ''
        cmd += ' -U{}'.format(type_of_non_orthog_filters) if type_of_non_orthog_filters is not None else ''
        cmd += ' -n{}'.format(number_of_scales) if number_of_scales is not None else ''
        cmd += ' -K' if suppress_last_scale else ''
        cmd += ' -k' if suppress_isolated_pixels else ''
        cmd += ' -C{}'.format(coef_detection_method) if coef_detection_method is not None else ''
        cmd += ' -s{}'.format(k_sigma_noise_threshold) if k_sigma_noise_threshold is not None else ''
        cmd += ' -m{}'.format(noise_model) if noise_model is not None else ''
        cmd += ' -p' if detect_only_positive_structure else ''
        cmd += ' -P' if suppress_positivity_constraint else ''
        cmd += ' -f{}'.format(type_of_filtering) if type_of_filtering is not None else ''
        cmd += ' -F{}'.format(first_detection_scale) if first_detection_scale is not None else ''
        cmd += ' -i{}'.format(number_of_iterations) if number_of_iterations is not None else ''
        cmd += ' -e{}'.format(epsilon) if epsilon is not None else ''
        cmd += ' -w{}'.format(support_file_name) if support_file_name is not None else ''
        cmd += ' -E{}'.format(precision) if precision is not None else ''

        cmd += ' -v' if verbose else ''
        self.label = "WT ({})".format(cmd)  # Name to show in plots

        cmd += ' "{}" {}'.format(input_file_path, mr_output_file_path)

        #cmd = 'mr_filter -K -k -C1 -s3 -m3 -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)
        #cmd = 'mr_filter -K -k -C1 -s3 -m2 -p -P -n{} "{}" {}'.format(number_of_scales, input_file_path, mr_output_file_path)

        if verbose:
            print()
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


    parser.add_argument("--type-of-filtering", "-f", type=int, metavar="INTEGER",
                        help="""Type of filtering:
                            1: Multiresolution Hard K-Sigma Thresholding
                            2: Multiresolution Soft K-Sigma Thresholding
                            3: Iterative Multiresolution Thresholding
                            4: Adjoint operator applied to the multiresolution support
                            5: Bivariate Shrinkage
                            6: Multiresolution Wiener Filtering
                            7: Total Variation + Wavelet Constraint
                            8: Wavelet Constraint Iterative Methods
                            9: Median Absolute Deviation (MAD) Hard Thesholding
                            10: Median Absolute Deviation (MAD) Soft Thesholding.
                            Default=1.""")

    parser.add_argument("--coef-detection-method", "-C", type=int, metavar="INTEGER",
                        help="""Coef_Detection_Method:
                            1: K-SigmaNoise Threshold
                            2: False Discovery Rate (FDR) Theshold
                            3: Universal Threshold
                            4: SURE Threshold
                            5: Multiscale SURE Threshold.
                            Default=1.""")

    parser.add_argument("--type-of-multiresolution-transform", "-t", type=int, metavar="INTEGER",
                        help="""Type of multiresolution transform:
                            1: linear wavelet transform: a trous algorithm
                            2: bspline wavelet transform: a trous algorithm
                            3: wavelet transform in Fourier space
                            4: morphological median transform
                            5: morphological minmax transform
                            6: pyramidal linear wavelet transform
                            7: pyramidal bspline wavelet transform
                            8: pyramidal wavelet transform in Fourier space: algo 1 (diff. between two resolutions)
                            9: Meyer's wavelets (compact support in Fourier space)
                            10: pyramidal median transform (PMT)
                            11: pyramidal laplacian
                            12: morphological pyramidal minmax transform
                            13: decomposition on scaling function
                            14: Mallat's wavelet transform (7/9 filters)
                            15: Feauveau's wavelet transform
                            16: Feauveau's wavelet transform without undersampling
                            17: Line Column Wavelet Transform (1D+1D)
                            18: Haar's wavelet transform
                            19: half-pyramidal transform
                            20: mixed Half-pyramidal WT and Median method (WT-HPMT)
                            21: undecimated diadic wavelet transform (two bands per scale)
                            22: mixed WT and PMT method (WT-PMT)
                            23: undecimated Haar transform: a trous algorithm (one band per scale)
                            24: undecimated (bi-) orthogonal transform (three bands per scale)
                            25: non orthogonal undecimated transform (three bands per scale)
                            26: Isotropic and compact support wavelet in Fourier space
                            27: pyramidal wavelet transform in Fourier space: algo 2 (diff. between the square of two resolutions)
                            28: Fast Curvelet Transform.
                            Default=2.""")

    parser.add_argument("--type-of-filters", "-T", type=int, metavar="INTEGER",
                        help="""Type of filters:
                            1: Biorthogonal 7/9 filters
                            2: Daubechies filter 4
                            3: Biorthogonal 2/6 Haar filters
                            4: Biorthogonal 2/10 Haar filters
                            5: Odegard 9/7 filters
                            6: 5/3 filter
                            7: Battle-Lemarie filters (2 vanishing moments)
                            8: Battle-Lemarie filters (4 vanishing moments)
                            9: Battle-Lemarie filters (6 vanishing moments)
                            10: User's filters
                            11: Haar filter
                            12: 3/5 filter
                            13: 4/4 Linar spline filters
                            14: Undefined sub-band filters.
                            Default=1.""")

    parser.add_argument("--type-of-non-orthog-filters", "-U", type=int, metavar="INTEGER",
                        help="""Type of non-orthogonal filters:
                            1: SplineB3-Id+H:  H=[1,4,6,4,1]/16, Ht=H, G=Id-H, Gt=Id+H
                            2: SplineB3-Id:  H=[1,4,6,4,1]/16, Ht=H, G=Id-H*H, Gt=Id
                            3: SplineB2-Id: H=4[1,2,1]/4, Ht=H, G=Id-H*H, Gt=Id
                            4: Harr/Spline POS: H=Haar,G=[-1/4,1/2,-1/4],Ht=[1,3,3,1]/8,Gt=[1,6,1]/4.
                            Default=2.""")

#         [-u number_of_undecimated_scales]
#             Number of undecimated scales used in the Undecimated Wavelet Transform
#             Default is all scale.
#
#         [-g sigma]
#             sigma = noise standard deviation
#             default is automatically estimated.
#
#         [-c gain,sigma,mean]
#             Poisson + readout noise, with:
#                 gain = gain of the CCD
#                 sigma = read-out noise standard deviation
#                 mean = read-out noise mean
#             default is no (Gaussian).

    parser.add_argument("--noise-model", "-m", type=int, metavar="INTEGER",
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
                            10: Poisson noise with few events. Default=1.""")

    parser.add_argument("--number-of-scales", "-n", type=int, metavar="integer",
                        help="Number of scales used in the multiresolution transform. Default=4.")

    parser.add_argument("--k-sigma-noise-threshold", "-s", type=float, metavar="FLOAT",
                        help="Thresholding at nsigma * SigmaNoise. Default=3.")

    parser.add_argument("--number-of-iterations", "-i", type=int, metavar="integer",
                        help="Maximum number of iterations. Default=10.")

    parser.add_argument("--epsilon", "-e", type=float, metavar="FLOAT",
                        help="Convergence parameter. Default=0.001000 or 0.000010 in case of poisson noise with few events.")
 
    parser.add_argument("--support-file-name", "-w", metavar="FILE",
                        help="Creates an image from the multiresolution support and save to disk.")

    parser.add_argument("--suppress-isolated-pixels", "-k", action="store_true",
                        help="Suppress isolated pixels in the support")

    parser.add_argument("--suppress-last-scale", "-K", action="store_true",
                        help="Suppress the last scale (to have background pixels = 0)")

    parser.add_argument("--detect-only-positive-structure", "-p", action="store_true",
                        help="Detect only positive structure")

    parser.add_argument("--precision", "-E", type=float, metavar="FLOAT",
                        help="Epsilon = precision for computing thresholds (only used in case of poisson noise with few events). Default=1.00e-03.")

#         [-S SizeBlock]
#             Size of the  blocks used for local variance estimation.
#             default is 7.
#
#         [-N NiterSigmaClip]
#             Iteration number used for local variance estimation.
#             default is 1.

    parser.add_argument("--first-detection-scale", "-F", type=int, metavar="INTEGER",
                        help="First scale used for the detection. Default=1.")

#         [-R RMS_Map_File_Name]
#              RMS Map (only used with -m 5 and -m 9 options).
 
    parser.add_argument("--suppress-positivity-constraint", "-P", action="store_true",
                        help="Suppress positivity constraint")

    parser.add_argument("--maximum-level-constraint", action="store_true",
                        help="Add the maximum level constraint. Max value is 255.")
 
#         [-B BackgroundModelImage]
#             Background Model Image: the background image is
#             subtracted during the filtering.
#             Default is no.
#
#         [-M Flat_Image]
#             Flat Image: The solution is corrected from the flat (i.e. Sol = Input / Flat)
#             Default is no.
#
#         [-h]
#             write info used for computing the probability map.
#             Default is no.
#
#         [-G RegulParam]
#              Regularization parameter for the TV method.
#              default is 0.100000
#
#         [-z]
#             Use virtual memory.
#                default limit size: 4
#                default directory: .
#
#         [-Z VMSize:VMDIR]
#             Use virtual memory.
#                VMSize = limit size (megabytes)
#                VMDIR = directory name
#

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    # COMMON OPTIONS

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", metavar="FILE",
                        help="The output file where to save plotted images")

    parser.add_argument("--output", "-o", metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    type_of_multiresolution_transform = args.type_of_multiresolution_transform
    type_of_filters = args.type_of_filters
    type_of_non_orthog_filters = args.type_of_non_orthog_filters
    number_of_scales = args.number_of_scales
    suppress_last_scale = args.suppress_last_scale
    suppress_isolated_pixels = args.suppress_isolated_pixels
    coef_detection_method = args.coef_detection_method
    k_sigma_noise_threshold = args.k_sigma_noise_threshold
    noise_model = args.noise_model
    detect_only_positive_structure = args.detect_only_positive_structure
    suppress_positivity_constraint = args.suppress_positivity_constraint
    type_of_filtering = args.type_of_filtering
    first_detection_scale = args.first_detection_scale 
    number_of_iterations = args.number_of_iterations 
    epsilon = args.epsilon 
    support_file_name = args.support_file_name 
    precision = args.precision 
    verbose = args.verbose

    benchmark_method = args.benchmark
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {
                "type_of_multiresolution_transform": type_of_multiresolution_transform,
                "type_of_filters": type_of_filters,
                "type_of_non_orthog_filters": type_of_non_orthog_filters,
                "number_of_scales": number_of_scales,
                "suppress_last_scale": suppress_last_scale,
                "suppress_isolated_pixels": suppress_isolated_pixels,
                "coef_detection_method": coef_detection_method,
                "k_sigma_noise_threshold": k_sigma_noise_threshold,
                "noise_model": noise_model,
                "detect_only_positive_structure": detect_only_positive_structure,
                "suppress_positivity_constraint": suppress_positivity_constraint,
                "type_of_filtering": type_of_filtering,
                "first_detection_scale": first_detection_scale,
                "number_of_iterations": number_of_iterations,
                "epsilon": epsilon,
                "support_file_name": support_file_name,
                "precision": precision,
                "verbose": verbose
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

