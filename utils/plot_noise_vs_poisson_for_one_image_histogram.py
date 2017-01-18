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


def parse_fits_files(fits_file_name):
    # Read the input file #########
    fits_images_dict, fits_metadata_dict = images.load_benchmark_images(fits_file_name)

    # Get images ##################
    input_img = fits_images_dict["input_image"]
    reference_img = fits_images_dict["reference_image"]

    pure_noise_image = input_img - reference_img

    return pure_noise_image, fits_metadata_dict


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

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The input image (FITS file) used to make statistics on the noise.")

    args = parser.parse_args()

    title = args.title
    logy = args.logy
    quiet = args.quiet
    input_file_path = args.fileargs[0]

    # FETCH NOISE #############################################################

    # Parse FITS file
    data_list, metadata_dict = parse_fits_files(input_file_path)

    if title is None:
        title = "Noise histogram for event {} on telescope {}".format(metadata_dict["event_id"], metadata_dict["tel_id"])

    if args.output is None:
        output_file_path = "noise_histogram_ev{}_tel{}.png".format(metadata_dict["event_id"], metadata_dict["tel_id"])
    else: 
        output_file_path = args.output

    # PLOT STATISTICS #########################################################

    print("Plotting...")

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))

    common.plot_hist1d(axis=ax1,
                       data_list=[np.array(data_list).flatten(),
                                  np.random.poisson(lam=2, size=40*40),
                                  np.random.poisson(lam=3, size=40*40)],
                       label_list=["Noise",
                                   r"Poisson dist. ($\lambda$=2)",
                                   r"Poisson dist. ($\lambda$=3)"],
                       logy=logy,
                       xlabel="Photoelectrons",
                       xylabel_fontsize=16,
                       title=title,
                       linear_xlabel_style=None,
                       linear_ylabel_style=None,
                       num_bins=None,
                       info_box_num_samples=False,
                       info_box_rms=False,
                       info_box_std=True)

    # Save file and plot ########

    plt.tight_layout()

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

