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

from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from datapipe.image import geometry_converter
from datapipe.image.kill_isolated_pixels import kill_isolated_pixels as scipy_kill_isolated_pixels
from datapipe.image.kill_isolated_pixels import kill_isolated_pixels_stats
from datapipe.image.kill_isolated_pixels import number_of_islands

from ctapipe.image.cleaning import tailcuts_clean

class Tailcut(AbstractCleaningAlgorithm):

    def __init__(self):
        super(Tailcut, self).__init__()
        self.label = "Tailcut"  # Name to show in plots

    def clean_image(self,
                    input_img,
                    high_threshold=10.,
                    low_threshold=8.,
                    kill_isolated_pixels=False,
                    verbose=False,
                    cam_id=None,
                    output_data_dict=None,
                    **kwargs):
        """Apply ctapipe's tail-cut image cleaning on ``.

        """

        if cam_id is None:
            raise Exception("cam_id have to be defined")    # TODO

        # 2D ARRAY (FITS IMAGE) TO CTAPIPE IMAGE ###############

        geom_1d = geometry_converter.get_geom1d(cam_id)
        img_1d = geometry_converter.image_2d_to_1d(input_img, cam_id)

        # APPLY TAILCUT CLEANING ##############################

        mask = tailcuts_clean(geom_1d,
                              img_1d,
                              picture_thresh=high_threshold,
                              boundary_thresh=low_threshold)
        img_1d[mask == False] = 0

        # CTAPIPE IMAGE TO 2D ARRAY (FITS IMAGE) ###############

        cleaned_img_2d = geometry_converter.image_1d_to_2d(img_1d, cam_id)

        # KILL ISOLATED PIXELS #################################

        img_cleaned_islands_delta_pe, img_cleaned_islands_delta_abs_pe, img_cleaned_islands_delta_num_pixels = kill_isolated_pixels_stats(cleaned_img_2d)
        img_cleaned_num_islands = number_of_islands(cleaned_img_2d)

        if output_data_dict is not None:
            output_data_dict["img_cleaned_islands_delta_pe"] = img_cleaned_islands_delta_pe
            output_data_dict["img_cleaned_islands_delta_abs_pe"] = img_cleaned_islands_delta_abs_pe
            output_data_dict["img_cleaned_islands_delta_num_pixels"] = img_cleaned_islands_delta_num_pixels
            output_data_dict["img_cleaned_num_islands"] = img_cleaned_num_islands

        if kill_isolated_pixels:
            if verbose:
                print("Kill isolated pixels")
            cleaned_img_2d = scipy_kill_isolated_pixels(cleaned_img_2d)

        return cleaned_img_2d


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with the tailcut algorithm.")

    parser.add_argument("--high_threshold", "-T", type=float, default=0, metavar="FLOAT", 
                        help="The 'high' threshold value")

    parser.add_argument("--low_threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The 'low' threshold value")

    parser.add_argument("--kill-isolated-pixels", action="store_true",
                        help="Suppress isolated pixels in the support (scipy implementation)")

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    # COMMON OPTIONS

    parser.add_argument("--debug", action="store_true",
                        help="Debug mode")

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

    debug = args.debug
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

    output_dict = cleaning_algorithm.run(cleaning_function_params,
                                         input_file_or_dir_path_list,
                                         benchmark_method,
                                         output_file_path,
                                         plot=plot,
                                         saveplot=saveplot,
                                         debug=debug)

if __name__ == "__main__":
    main()

