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
  ./denoising_with_fft.py -t 0.0001 -s ./test.fits
  ./denoising_with_fft.py -t 0.001 ./test.fits
  ipython3 -- ./denoising_with_fft.py -t 0.0001 -s ./test.fits

This snippet requires Numpy, Scipy, Matplotlib and PIL/Pillow Python libraries.

Additional documentation:
- Numpy implementation: http://docs.scipy.org/doc/numpy/reference/routines.fft.html
- Scipy implementation: http://docs.scipy.org/doc/scipy/reference/fftpack.html
"""

__all__ = ['fft']

import argparse
import datetime
import json
import os
import numpy as np
import time

import datapipe.denoising
from datapipe.benchmark import assess
from datapipe.io import images


def fft(input_img, shift=False, threshold=0., base_file_path="fft", verbose=False):
    """
    Do the fourier transform.
    """

    base_file_path="fft"

    transformed_img = np.fft.fft2(input_img)

    if shift:
        transformed_img = np.fft.fftshift(transformed_img)

    if verbose:
        images.plot(np.log10(abs(transformed_img)),
                    title="Fourier coefficients before filtering")
        images.mpl_save(np.log10(abs(transformed_img)),
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

    if verbose:
        images.plot(np.log10(abs(filtered_transformed_img)),
                    title="Fourier coefficients after filtering")
        images.mpl_save(np.log10(abs(filtered_transformed_img)),
                        "{}_dft_fourier_coefficients_after_filtering.pdf".format(base_file_path),
                        title="Fourier coefficients after filtering")

    # Do the reverse transform #############

    if shift:
        filtered_transformed_img = np.fft.ifftshift(filtered_transformed_img)

    cleaned_img_complex = np.fft.ifft2(filtered_transformed_img)
    
    cleaned_img = abs(cleaned_img_complex)

    return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with DFT.")

    parser.add_argument("--shift", "-s", action="store_true", default=False,
                        help="Shift the zero to the center")

    parser.add_argument("--threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The threshold value (between 0 and 1)")

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

    shift = args.shift
    threshold = args.threshold
    benchmark_method = args.benchmark
    plot = args.plot
    saveplot = args.saveplot
    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_fft_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {"shift": shift, "threshold": threshold}
    cleaning_algorithm_label = "FFT"

    datapipe.denoising.run(fft,
                           cleaning_function_params,
                           input_file_or_dir_path_list,
                           benchmark_method,
                           output_file_path,
                           cleaning_algorithm_label,
                           plot,
                           saveplot)


if __name__ == "__main__":
    main()

