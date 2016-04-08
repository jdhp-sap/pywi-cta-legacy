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
Denoise FITS and PNG images with the tailcut algorithm.

Example usages:
  ./denoising_with_tailcut.py -h
  ./denoising_with_tailcut.py -T 0.5 -t 0.1 ./test.fits
  ./denoising_with_tailcut.py -T 0.5 -t 0.1 ./test.fits
  ipython3 -- ./denoising_with_tailcut.py -t 0.0001 -s ./test.fits

This snippet requires Numpy, Matplotlib and PIL/Pillow Python libraries.
"""

import argparse
import os
import numpy as np

import utils

def tailcut(img, high_threshold=4.25, low_threshold=2.25, base_file_path="tailcut"):

    # COMPUTE MASKS #######################################

    # TODO
#    img_sigma = np.std(img)
    max_value = np.max(img)

    # TODO
#    high_mask = (img > (img_sigma * high_threshold)  
#    low_mask = (img > (img_sigma * low_threshold)  
    high_mask = (img > (max_value * high_threshold)
    low_mask =  (img > (max_value * low_threshold))

    # MERGE MASKS #########################################

    final_mask = high_mask

    boundary_ids = []
    #for pix_id in geom.pix_id[low_mask]:                # TODO
    #    if final_mask[geom.neighbors[pix_id]].any():    # TODO
    #        boundary_ids.append(pix_id)

    final_mask[boundary_ids] = True

    # PLOT MASK ###########################################

    utils.plot_image(final_mask,
                     title="Tailcut mask")
    utils.save_image(final_mask,
                     "{}_tailcut_mask.pdf".format(base_file_path),
                     title="Tailcut mask")

    # APPLY MASK ##########################################

    filtered_img = img * final_mask

    return filtered_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS and PNG images with the tailcut algorithm.")

    parser.add_argument("--high_threshold", "-T", type=float, default=0, metavar="FLOAT", 
                        help="The 'high' threshold value (between 0 and 1)")
    parser.add_argument("--low_threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The 'low' threshold value (between 0 and 1)")
    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The file image to process (FITS or PNG)")
    args = parser.parse_args()

    high_threshold = args.high_threshold
    low_threshold = args.low_threshold
    input_file_path = args.fileargs[0]

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    # READ THE INPUT FILE ######################################################

    input_img = utils.get_image_array_from_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # TAILCUT FILTER ##########################################################

    filtered_img = tailcut(input_img, high_threshold, low_threshold)

    utils.plot_image(filtered_img,
                     title="Denoised image")
    utils.save_image(filtered_img,
                     "{}_tailcut_denoised.pdf".format(base_file_path),
                     title="Denoised image")


if __name__ == "__main__":
    main()

