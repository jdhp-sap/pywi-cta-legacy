#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
import numpy as np
from matplotlib import pyplot as plt
import os


def parse_json_file(json_file_path):
    with open(json_file_path, "r") as fd:
        json_data = json.load(fd)
    return json_data


def extract_metadata_list(json_dict, key1, key2, exclude_aborted, aborted_only):
    io_list = json_dict["io"]

    if exclude_aborted:
        json_data = [(image_dict[key1], image_dict[key2]) for image_dict in io_list if "error" not in image_dict]
    elif aborted_only:
        json_data = [(image_dict[key1], image_dict[key2]) for image_dict in io_list if "error" in image_dict]
    else:
        json_data = [(image_dict[key1], image_dict[key2]) for image_dict in io_list]

    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--exclude-aborted", action="store_true", default=False,
                        help="Ignore values from aborted images")

    parser.add_argument("--aborted-only", action="store_true", default=False,
                        help="Only consider aborted images")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--key1", metavar="KEY", 
                        help='The key of the first value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

    parser.add_argument("--key2", metavar="KEY", 
                        help='The key of the second value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    title = args.title
    quiet = args.quiet
    json_file_path = args.fileargs[0]

    key1 = args.key1
    key2 = args.key2

    if args.output is None:
        base_file_path = os.path.basename(json_file_path)
        base_file_path = os.path.splitext(base_file_path)[0]
        output_file_path = "metadata_correlation_{}_{}_{}.pdf".format(base_file_path, key1, key2)
    else:
        output_file_path = args.output

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    # FETCH SCORE #############################################################

    json_dict = parse_json_file(json_file_path)

    metadata_array = np.array(extract_metadata_list(json_dict, key1, key2, exclude_aborted, aborted_only))
    label = json_dict["label"]

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    ax1.plot(metadata_array[:,0], metadata_array[:,1], '.', alpha=0.2)


    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        if exclude_aborted:
            errors_str = "exclude errors"
        elif aborted_only:
            errors_str = "errors only"
        else:
            errors_str = None

        if errors_str is not None:
            ax1.set_title("{} - {} correlation ({})".format(key1, key2, errors_str), fontsize=20)
        else:
            ax1.set_title("{} - {} correlation".format(key1, key2), fontsize=20)

    # Info box
    ax1.text(0.95, 0.92,
            "{} images".format(metadata_array.shape[0]),
            verticalalignment = 'top',
            horizontalalignment = 'right',
            transform = ax1.transAxes,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})


    ax1.set_xlabel(key1, fontsize=20)
    ax1.set_ylabel(key2, fontsize=20)

    plt.setp(ax1.get_xticklabels(), fontsize=14)
    plt.setp(ax1.get_yticklabels(), fontsize=14)

    if logx:
        ax1.set_xscale("log")               # Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    if logy:
        ax1.set_yscale("log")               # Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()


