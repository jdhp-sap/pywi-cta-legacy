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

import argparse
import os
import numpy as np

import utils

def main():

    # PARSE OPTIONS ###############################################################

    parser = argparse.ArgumentParser(description="Denoise FITS and PNG images with Wavelet Transform.")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")
    parser.add_argument("filearg", nargs=1, metavar="FILE",
                        help="The file image to process (FITS or PNG)")

    args = parser.parse_args()

    number_of_scales = args.number_of_scales
    input_file_path = args.filearg[0]

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]
    mr_output_file_path = base_file_path + "_mr_planes.fits"


    # READ THE INPUT FILE #########################################################

    input_img = utils.get_image_array_from_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # EXECUTE MR_TRANSFORM ########################################################

    # TODO: improve the following lines
    cmd = 'mr_transform -n{} "{}" out'.format(number_of_scales, input_file_path)
    os.system(cmd)

    # TODO: improve the following lines
    cmd = "mv out.mr {}".format(mr_output_file_path)
    os.system(cmd)


    # READ THE MR_TRANSFORM OUTPUT FILE ###########################################

    output_imgs = utils.get_image_array_from_file(mr_output_file_path)

    if output_imgs.ndim != 3:
        raise Exception("Unexpected error: the output FITS file should contain a 3D array.")


    # DENOISE THE INPUT IMAGE WITH MR_TRANSFORM PLANES ############################

    denoised_img = np.zeros(input_img.shape)

    for img_index, img in enumerate(output_imgs):

        if img_index < (len(output_imgs) - 1):  # All planes except the last one

            # Compute the standard deviation of the plane ###########

            img_sigma = np.std(img)

            # Apply a threshold on the plane ########################

            # Remark: "abs(img) > (img_sigma * 3.)" should be the correct way to
            # make the image mask, but sometimes results looks better when all
            # negative coefficients are dropped ("img > (img_sigma * 3.)")

            #img_mask = abs(img) > (img_sigma * 3.)  
            img_mask = img > (img_sigma * 3.)
            filtered_img = img * img_mask

            utils.save_image(img,
                             "{}_wt_plane{}.pdf".format(base_file_path, img_index),
                             title="Plane {}".format(img_index))
            utils.save_image(img_mask,
                             "{}_wt_plane{}_mask.pdf".format(base_file_path, img_index),
                             title="Binary mask for plane {}".format(img_index))
            utils.save_image(filtered_img,
                             "{}_wt_plane{}_filtered.pdf".format(base_file_path, img_index),
                             title="Filtered plane {}".format(img_index))

            utils.plot_image(img, title="Plane {}".format(img_index))
            utils.plot_image(img_mask, title="Binary mask for plane {}".format(img_index))
            utils.plot_image(filtered_img, title="Filtered plane {}".format(img_index))

            # Sum the plane #########################################

            denoised_img = denoised_img + filtered_img

        else:   # The last plane should be kept unmodified

            utils.save_image(img,
                             "{}_wt_plane{}.pdf".format(base_file_path, img_index),
                             title="Plane {}".format(img_index))
            utils.plot_image(img, title="Plane {}".format(img_index))

            # Sum the last plane ####################################

            denoised_img = denoised_img + img

    utils.save_image(input_img,
                     "{}.pdf".format(base_file_path),
                     title="Original image")
    utils.save_image(denoised_img,
                     "{}_wt_denoised.pdf".format(base_file_path),
                     title="Filtered image")

    utils.plot_image(input_img, title="Original image")
    utils.plot_image(denoised_img, title="Denoised image")


if __name__ == "__main__":
    main()

