#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import json
#import math
import os

import matplotlib.pyplot as plt
import numpy as np

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5


def extract_data_list(json_dict, key, exclude_aborted, aborted_only):
    io_list = json_dict["io"]

    if exclude_aborted:
        json_data = [image_dict[key] for image_dict in io_list if "error" not in image_dict]
    elif aborted_only:
        json_data = [image_dict[key] for image_dict in io_list if "error" in image_dict]
    else:
        json_data = [image_dict[key] for image_dict in io_list]

    return json_data


def plot_hist(axis, data_array, logx, logy):
    """
    """

    if logx:
        # Setup the logarithmic scale on the X axis
        vmin = np.log10(data_array.min())
        vmax = np.log10(data_array.max())
        bins = np.logspace(vmin, vmax, 50) # Make a range from 10**vmin to 10**vmax
    else:
        bins = 50

    res_tuple = axis.hist(data_array,
                          bins=bins,
                          log=logy,               # Set log scale on the Y axis
                          histtype=HIST_TYPE,
                          alpha=ALPHA)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--key", "-k", required=True, metavar="STRING",
                        help='The key of the value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

    parser.add_argument("--exclude-aborted", action="store_true", default=False,
                        help="Ignore values from aborted images")

    parser.add_argument("--aborted-only", action="store_true", default=False,
                        help="Only consider aborted images")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--tight", action="store_true", default=False,
                        help="Optimize the X axis usage")

    parser.add_argument("--output", "-o", default=None, metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None, metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    key = args.key
    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    tight = args.tight
    title = args.title
    quiet = args.quiet
    json_file_path = args.fileargs[0]

    if args.output is None:
        base_file_path = os.path.basename(json_file_path)
        base_file_path = os.path.splitext(base_file_path)[0]
        output_file_path = "{}_{}.pdf".format(base_file_path, key)
    else:
        output_file_path = args.output

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)

    data_array = np.array(extract_data_list(json_dict, key, exclude_aborted, aborted_only))
    label = json_dict["label"]

    print("{} images".format(data_array.shape[0]))
    print("min:", data_array.min())
    print("max:", data_array.max())
    print("mean:", data_array.mean())

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    plot_hist(ax1, data_array, logx, logy)

    if tight:
        min_abscissa = data_array.min()
        max_abscissa = data_array.max()
        ax1.set_xlim(xmin=min_abscissa)
        ax1.set_xlim(xmax=max_abscissa)

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
            ax1.set_title("{} ({}) - {}".format(key, errors_str, label), fontsize=20)
        else:
            ax1.set_title("{} - {}".format(key, label), fontsize=20)

    # Info box
    ax1.text(0.95, 0.92,
            "{} images".format(data_array.shape[0]),
            verticalalignment = 'top',
            horizontalalignment = 'right',
            transform = ax1.transAxes,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})


    ax1.set_xlabel(key, fontsize=20)
    ax1.set_ylabel("Count", fontsize=20)

    plt.setp(ax1.get_xticklabels(), fontsize=14)
    plt.setp(ax1.get_yticklabels(), fontsize=14)

    if logx:
        ax1.set_xscale("log")               # Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    if not logy:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

