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
Denoise FITS and PNG images with Discrete Fourier Transform.

This script originally came from
https://github.com/jeremiedecock/snippets/blob/master/python/numpy/fft_transform/fft2.py.

Example usages:
  ./denoising_with_fft.py -h
  ./denoising_with_fft.py -t 0.0001 -s ./test.jpeg
  ./denoising_with_fft.py -t 0.001 ./test.jpeg
  ipython3 -- ./denoising_with_fft.py -t 0.0001 -s ./test.jpeg

This snippet requires Numpy, Scipy, Matplotlib and PIL/Pillow Python libraries.

Additional documentation:
- Numpy implementation: http://docs.scipy.org/doc/numpy/reference/routines.fft.html
- Scipy implementation: http://docs.scipy.org/doc/scipy/reference/fftpack.html
"""

import argparse
import os
import numpy as np

import utils

def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with DFT.")

    parser.add_argument("--shift", "-s", action="store_true", default=False,
                        help="Shift the zero to the center")
    parser.add_argument("--threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The threshold value (between 0 and 1)")
    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The file image to process (FITS or PNG)")
    args = parser.parse_args()

    shift = args.shift
    threshold = args.threshold
    input_file_path = args.fileargs[0]

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    # READ THE INPUT FILE ######################################################

    input_img = utils.get_image_array_from_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # FOURIER TRANSFORM WITH NUMPY ############################################

    # Do the fourier transform #############

    transformed_img = np.fft.fft2(input_img)

    if shift:
        transformed_img = np.fft.fftshift(transformed_img)

    utils.plot_image(np.log10(abs(transformed_img)),
                     title="Fourier coefficients before filtering")
    utils.save_image(np.log10(abs(transformed_img)),
                     "{}_dft_fourier_coefficients_before_filtering.pdf".format(base_file_path),
                     title="Fourier coefficients before filtering")


    # Compute the standard deviation of the plane ###########

    # TODO
#    img_sigma = np.std(transformed_img)
    max_value = np.max(abs(transformed_img))

    # Apply a threshold on the transformed image ############

    # TODO
#    img_mask = abs(transformed_img) > (img_sigma * 3.)  
    img_mask =  abs(transformed_img) > (max_value * threshold)
    filtered_transformed_img = transformed_img * img_mask

    utils.plot_image(np.log10(abs(filtered_transformed_img)),
                     title="Fourier coefficients after filtering")
    utils.save_image(np.log10(abs(filtered_transformed_img)),
                     "{}_dft_fourier_coefficients_after_filtering.pdf".format(base_file_path),
                     title="Fourier coefficients after filtering")


    # Do the reverse transform #############

    if shift:
        filtered_transformed_img = np.fft.ifftshift(filtered_transformed_img)

    filtered_img = np.fft.ifft2(filtered_transformed_img)

    utils.plot_image(abs(filtered_img),
                     title="Denoised image")
    utils.save_image(abs(filtered_img),
                     "{}_dft_denoised.pdf".format(base_file_path),
                     title="Denoised image")


if __name__ == "__main__":
    main()

