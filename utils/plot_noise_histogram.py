#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on the noise of benchmark FITS files.
"""

import common_functions as common

import argparse
from matplotlib import pyplot as plt
import os

import math
import numpy as np

from datapipe.io import images


def parse_fits_files(fits_file_name_list, progress_bar=True):
    fits_noise_list = []

    for file_index, file_name in enumerate(fits_file_name_list):

        # Read the input file #########
        fits_images_dict, fits_metadata_dict = images.load_benchmark_images(file_name)

        # Get images ##################
        input_img = fits_images_dict["input_image"]
        reference_img = fits_images_dict["reference_image"]

        pure_noise_image = input_img - reference_img
        fits_noise_list.append(pure_noise_image)

        # Progress bar ################
        if progress_bar:
            num_files = len(fits_file_name_list)
            relative_steps = math.ceil(num_files / 100.)

            if (file_index % relative_steps) == 0:
                progress_str = "{:.2f}% ({}/{})".format((file_index + 1)/num_files * 100,
                                                         file_index + 1,
                                                         num_files)
                print(progress_str)

    return fits_noise_list 


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on the noise of benchmark FITS files.")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("fileargs", nargs=1, metavar="DIRECTORY",
                        help="The directory containing input images (FITS files) used to make statistics on the noise.")

    args = parser.parse_args()

    title = args.title
    logy = args.logy
    quiet = args.quiet
    notebook = args.notebook
    input_directory_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "noise_histogram.pdf"
    else:
        output_file_path = args.output

    # FETCH NOISE #############################################################

    # Parse the input directory
    fits_file_name_list = common.get_fits_files_list(input_directory_path)

    # Parse FITS files
    data_list = parse_fits_files(fits_file_name_list, progress_bar=not notebook)

    # PLOT STATISTICS #########################################################

    if not notebook:
        print("Plotting...")

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))

    common.plot_hist1d(axis=ax1,
                       data_list=[np.array(data_list).flatten()],
                       label_list=[],
                       logy=logy,
                       xlabel="Photoelectrons",
                       xylabel_fontsize=16,
                       title=title,
                       linear_xlabel_style=None,
                       linear_ylabel_style=None,
                       num_bins=None,
                       info_box_rms=False,
                       info_box_std=True)

    # Save file and plot ########

    if not notebook:
        plt.tight_layout()

        plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

