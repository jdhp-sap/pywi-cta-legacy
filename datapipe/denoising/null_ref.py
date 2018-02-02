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
Denoise FITS and PNG images with the "Null" algorithm (actually does nothing).

Example usages:
  ./datapipe/denoising/null.py -h
  ./datapipe/denoising/null.py ./test.fits
  ipython3 -- ./datapipe/denoising/null.py ./test.fits
"""

import argparse
import copy
import json
import numpy as np

import datapipe.denoising
from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm


class Null(AbstractCleaningAlgorithm):

    def __init__(self):
        super(Null, self).__init__()
        self.label = "Null"  # Name to show in plots

    def clean_image(self, img, output_data_dict=None, **kwargs):
        return copy.deepcopy(img)


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='"Denoise" FITS images with the "null" algorithm (which does nothing but which is usefull for CSV conversion).')


    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--label", "-l", default=None,
                        metavar="STRING",
                        help="The label attached to the produced results")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")


    args = parser.parse_args()

    benchmark_method = args.benchmark
    label = args.label
    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_{}_benchmark_{}.json".format(label if label is not None else "null", benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {}

    cleaning_algorithm = Null()

    if label is not None:
        cleaning_algorithm.label = label

    cleaning_algorithm.run(cleaning_function_params,
                           input_file_or_dir_path_list,
                           benchmark_method,
                           output_file_path,
                           ref_img_as_input=True)


if __name__ == "__main__":
    main()

