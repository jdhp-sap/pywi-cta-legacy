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
import datetime
import json
import os
import numpy as np
import time

import datapipe.denoising
from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from datapipe.benchmark import assess
from datapipe.io import images

from datapipe.image.kill_isolated_pixels import kill_isolated_pixels as scipy_kill_isolated_pixels

import ctapipe.io
from ctapipe.image.cleaning import tailcuts_clean, dilate

class Tailcut(AbstractCleaningAlgorithm):

    def __init__(self):
        super(Tailcut, self).__init__()
        self.label = "Tailcut"  # Name to show in plots

    def clean_image(self,
                    input_img,
                    high_threshold=10.,
                    low_threshold=8.,
                    kill_isolated_pixels=False,
                    verbose=False):
        """
        vim ./ctapipe/reco/cleaning.py ./ctapipe/reco/tests/test_cleaning.py ./ctapipe/tools/camdemo.py ./examples/read_hessio_single_tel.py
        """

        # TODO: clean these following hard coded values for Astri
        num_pixels_x = 40
        num_pixels_y = 40
        range_x = (-0.142555996776, 0.142555996776)
        range_y = (-0.142555996776, 0.142555996776)

        #geom = ctapipe.io.CameraGeometry.from_name("astri", 1)  # TODO

        geom = ctapipe.io.camera.make_rectangular_camera_geometry(num_pixels_x,
                                                                  num_pixels_y,
                                                                  range_x,
                                                                  range_y)

        signal = np.ravel(input_img)

        mask = tailcuts_clean(geom,
                              signal,                   # TODO
                              1,
                              picture_thresh=high_threshold,
                              boundary_thresh=low_threshold)

        ##if True not in mask: continue       # TODO ?????
        #dilate(geom, mask)                   # TODO ?

        signal[mask == False] = 0

        #                for ii in range(3):
        #                    reco.cleaning.dilate(geom, cleanmask)
        #                    image[cleanmask == 0] = 0  # zero noise pixels

        cleaned_img = signal.reshape(num_pixels_x, num_pixels_y)

        # KILL ISOLATED PIXELS #################################

        if kill_isolated_pixels:
            if verbose:
                print("Kill isolated pixels")
            cleaned_img = scipy_kill_isolated_pixels(cleaned_img)

        return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with the tailcut algorithm.")

    parser.add_argument("--high_threshold", "-T", type=float, default=0, metavar="FLOAT", 
                        help="The 'high' threshold value (between 0 and 1)")

    parser.add_argument("--low_threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The 'low' threshold value (between 0 and 1)")

    parser.add_argument("--kill-isolated-pixels", action="store_true",
                        help="Suppress isolated pixels in the support (scipy implementation)")

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    # COMMON OPTIONS

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

    high_threshold = args.high_threshold
    low_threshold = args.low_threshold
    kill_isolated_pixels = args.kill_isolated_pixels
    verbose = args.verbose

    benchmark_method = args.benchmark
    label = args.label
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_tailcut_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {
                "high_threshold": high_threshold,
                "low_threshold": low_threshold,
                "kill_isolated_pixels": kill_isolated_pixels,
                "verbose": verbose
            }

    cleaning_algorithm = Tailcut()

    if label is not None:
        cleaning_algorithm.label = label

    cleaning_algorithm.run(cleaning_function_params,
                           input_file_or_dir_path_list,
                           benchmark_method,
                           output_file_path,
                           plot,
                           saveplot)


if __name__ == "__main__":
    main()

