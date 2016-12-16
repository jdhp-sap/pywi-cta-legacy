#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
from matplotlib import pyplot as plt
import os

import math

import copy

from datapipe.io import images


def get_fits_files_list(directory_path):

    # Parse the input directory
    print("Parsing", directory_path)

    fits_file_name_list = [os.path.join(directory_path, file_name)
                           for file_name
                           in os.listdir(directory_path)
                           if os.path.isfile(os.path.join(directory_path, file_name))
                           and file_name.endswith((".fits", ".fit"))]

    return fits_file_name_list


def parse_fits_files(fits_file_name_list, mc_energy_min, mc_energy_max):
    print("Parsing images in range ]{:.2f},{:.2f}] TeV...".format(mc_energy_min, mc_energy_max))

    fits_noise_list = []

    # Parse the input files
    mc_energy_unit = None

    for file_index, file_name in enumerate(fits_file_name_list):

        # Read the input file #########
        fits_images_dict, fits_metadata_dict = images.load_benchmark_images(file_name)

        if mc_energy_min < fits_metadata_dict["mc_energy"] <= mc_energy_max:
            # Sanity check ################
            if mc_energy_unit is None:
                mc_energy_unit = fits_metadata_dict["mc_energy_unit"] # TODO
            else:
                if mc_energy_unit != fits_metadata_dict["mc_energy_unit"]:
                    raise Exception("Inconsistent data")

            # Get images ##################
            input_img = fits_images_dict["input_image"]
            reference_img = fits_images_dict["reference_image"]

            pure_noise_image = input_img - reference_img
            fits_noise_list.append(pure_noise_image)

        # Progress bar ################
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

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

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

    parser.add_argument("fileargs", nargs=1, metavar="DIRECTORY",
                        help="The directory containing input images (FITS files) used to make statistics on the noise.")

    args = parser.parse_args()

    title = args.title
    logy = args.logy
    quiet = args.quiet
    input_directory_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "noise_histogram.pdf"
    else:
        output_file_path = args.output

    # FETCH NOISE #############################################################

    # Parse the input directory
    fits_file_name_list = get_fits_files_list(input_directory_path)

    # Parse FITS files
    data_list1 = parse_fits_files(fits_file_name_list,   0.1,    1.0)  # 1 TeV to 10 TeV
    data_list2 = parse_fits_files(fits_file_name_list,   1.0,   10.0)  # 1 TeV to 10 TeV
    data_list3 = parse_fits_files(fits_file_name_list,  10.0,  100.0)  # 10 TeV to 100 TeV
    data_list4 = parse_fits_files(fits_file_name_list, 100.0, 1000.0)  # 100 TeV to 1000 TeV

    # PLOT STATISTICS #########################################################

    print("Plotting...")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))

    common.plot_hist1d(axis=ax1,
                       data_list=data_list1,
                       label_list=[],
                       logy=logy)

    common.plot_hist1d(axis=ax2,
                       data_list=data_list2,
                       label_list=[],
                       logy=logy)

    common.plot_hist1d(axis=ax3,
                       data_list=data_list3,
                       label_list=[],
                       logy=logy)

    common.plot_hist1d(axis=ax4,
                       data_list=data_list4,
                       label_list=[],
                       logy=logy)

    ax1.set_title("100 GeV to 1 TeV", fontsize=20)
    ax2.set_title("1 TeV to 10 TeV", fontsize=20)
    ax3.set_title("10 TeV to 100 TeV", fontsize=20)
    ax4.set_title("100 TeV to 1000 TeV", fontsize=20)
    
    if title is not None:
        plt.suptitle(title, fontsize=20)
    else:
        plt.suptitle(metric, fontsize=20)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

