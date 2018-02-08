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
import numpy as np
import os
import time

import datapipe.denoising
from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from datapipe.benchmark import assess
from datapipe.io import images


# EXCEPTIONS #################################################################

class MrTransformError(Exception):
    pass

class WrongDimensionError(MrTransformError):
    """Exception raised when trying to save a FITS with more than 3 dimensions
    or less than 2 dimensions.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        super(WrongDimensionError, self).__init__("Unexpected error: the output FITS file should contain a 2D array.")


##############################################################################

def wavelet_transform(input_img,
                      num_scales=4,
                      tmp_files_directory=".",       # "/Volumes/ramdisk"
                      noise_distribution=None,
                      **kwargs):
    """
    Do the wavelet transform.
    """

    input_img = input_img.copy()

    if input_img.ndim != 2:
        raise WrongDimensionError()

    input_file_path = os.path.join(tmp_files_directory, ".tmp_{}_{}_in.fits".format(os.getpid(), time.time()))
    mr_output_file_path = os.path.join(tmp_files_directory, ".tmp_{}_{}_out.fits".format(os.getpid(), time.time()))

    # INJECT NOISE IN NAN ##################################

    # See https://stackoverflow.com/questions/29365194/replacing-missing-values-with-random-in-a-numpy-array
    nan_mask = np.isnan(input_img)

    #print(input_img)
    #images.plot(input_img, "In")
    #images.plot(nan_mask, "Mask")

    if noise_distribution is not None:
        nan_noise_size = np.count_nonzero(nan_mask)
        input_img[nan_mask] = noise_distribution.rvs(size=nan_noise_size)

    #print(input_img)
    #images.plot(input_img, "Noise injected")

    try:
        # WRITE THE INPUT FILE (FITS) ##########################

        images.save(input_img, input_file_path)

        # EXECUTE MR_TRANSFORM #################################

        cmd = 'mr_transform -n{} "{}" {}'.format(num_scales, input_file_path, mr_output_file_path)
        os.system(cmd)

        cmd = "mv {}.mr {}".format(mr_output_file_path, mr_output_file_path)
        os.system(cmd)

        # READ THE MR_TRANSFORM OUTPUT FILE ####################

        plan_imgs = images.load(mr_output_file_path, 0)

        # CHECK RESULT #########################################

        if plan_imgs.ndim != 3:
            raise Exception("Unexpected error: the output FITS file should contain a 3D array.")

    finally:
        # REMOVE FITS FILES ####################################

        os.remove(input_file_path)
        os.remove(mr_output_file_path)
    
    return plan_imgs


class WaveletTransform(AbstractCleaningAlgorithm):

    def __init__(self):
        super().__init__()
        self.label = "WT (mr_transform)"  # Name to show in plots

    def clean_image(self, input_img, num_scales=4,
                    noise_distribution=None,
                    tmp_files_directory=".",       # "/Volumes/ramdisk"
                    output_data_dict=None):
        """
        Do the wavelet transform.

        mr_filter
        -K 
        -k
        -F2
        -C1
        -s3
        -m2  (a essayer ou -m10)

        eventuellement -w pour le debug
        """

        plan_imgs = wavelet_transform(input_img, num_scales, noise_distribution)

        # DENOISE THE INPUT IMAGE WITH MR_TRANSFORM PLANES #####

        denoised_img = np.zeros(input_img.shape)

        for img_index, img in enumerate(plan_imgs):

            if img_index < (len(plan_imgs) - 1):  # All planes except the last one

                # Compute the standard deviation of the plane ##

                img_sigma = np.std(img)

                # Apply a threshold on the plane ###############

                # Remark: "abs(img) > (img_sigma * 3.)" should be the correct way to
                # make the image mask, but sometimes results looks better when all
                # negative coefficients are dropped ("img > (img_sigma * 3.)")

                #img_mask = abs(img) > (img_sigma * 3.)  
                img_mask = img > (img_sigma * 3.)
                cleaned_img = img * img_mask

                if self.verbose:
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

                denoised_img += cleaned_img

            else:   # The last plane should be kept unmodified

                if self.verbose:
                    images.mpl_save(img,
                                    "{}_wt_plane{}.pdf".format(base_file_path, img_index),
                                    title="Plane {}".format(img_index))
                    images.plot(img, title="Plane {}".format(img_index))

                # Sum the last plane ###########################

                denoised_img += cleaned_img
        
        return denoised_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--num_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")

    # COMMON OPTIONS

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    parser.add_argument("--debug", action="store_true",
                        help="Debug mode")

    parser.add_argument("--max-images", type=int, metavar="INTEGER", 
                        help="The maximum number of images to process")

    parser.add_argument("--telid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified telescope")

    parser.add_argument("--camid", metavar="STRING", 
                        help="Only process images from the specified camera")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--label", "-l", default=None,
                        metavar="STRING",
                        help="The label attached to the produced results")

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

    num_scales = args.num_scales

    verbose = args.verbose
    debug = args.debug
    max_images = args.max_images
    tel_id = args.telid
    cam_id = args.camid
    benchmark_method = args.benchmark
    label = args.label
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {"num_scales": num_scales}

    cleaning_algorithm = WaveletTransform()

    if verbose:
        cleaning_algorithm.verbose = True

    if label is not None:
        cleaning_algorithm.label = label

    output_dict = cleaning_algorithm.run(cleaning_function_params,
                                         input_file_or_dir_path_list,
                                         benchmark_method,
                                         output_file_path,
                                         plot=plot,
                                         saveplot=saveplot,
                                         max_num_img=max_images,
                                         tel_id=tel_id,
                                         cam_id=cam_id,
                                         debug=debug)

if __name__ == "__main__":
    main()

