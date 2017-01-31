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
Plot a FITS file.

Example usages:
  ./utils/plot_image.py -h
  ./utils/plot_image.py ./test.fits
  ipython3 -- ./utils/plot_image.py ./test.fits
"""

import common_functions as common

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from datapipe.io import images

##############################################

def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Plot a FITS file.")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None, metavar="FILE",
                        help="The output file path (image file)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The files image to process (FITS).")

    args = parser.parse_args()

    quiet = args.quiet
    output = args.output
    input_file_path = args.fileargs[0]

    # READ THE INPUT FILE #####################################################

    fits_images_dict, fits_metadata_dict = images.load_benchmark_images(input_file_path)

    reference_img = fits_images_dict["reference_image"]
    pixels_position = fits_images_dict["pixels_position"]

    # ASSESS OR PRINT THE CLEANED IMAGE #######################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(9, 9))

    common.plot_image_meter(ax1, reference_img, pixels_position, "Reference image")
    common.plot_ellipse_shower_on_image_meter(ax1, reference_img, pixels_position)

    # PLOT AND SAVE ###########################################################

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    if output is None:
        output = "{}.png".format(base_file_path)

    plt.savefig(output, bbox_inches='tight')

    if not quiet:
        plt.show()


if __name__ == "__main__":
    main()

