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
... TODO
"""

__all__ = ['export_pixel_mask']

import argparse
import numpy as np

from datapipe.io import images

def export_pixel_mask(input_file_path, output_file_path):
    fits_images_dict, fits_metadata_dict = images.load_benchmark_images(input_file_path)
    mask = fits_images_dict["pixels_mask"].astype(np.uint8, copy=True)
    images.save(mask, output_file_path)


def main():

    # PARSE OPTIONS ###########################################################

    desc = "Export the pixel mask in a FITS file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--output", "-o",
                        metavar="FILE",
                        help="The output FITS file")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The FITS file to process")

    args = parser.parse_args()

    output_file_path = args.output
    input_file_path = args.fileargs[0]

    export_pixel_mask(input_file_path , output_file_path)


if __name__ == "__main__":
    main()

