#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5


def extract_execution_time_list(json_dict):
    io_list = json_dict["io"]
    json_data = [image_dict["execution_time"] for image_dict in io_list if "execution_time" in image_dict]
    return json_data


def plot_hist(axis, data_list, label_list, logx, logy, overlaid):
    """
    """

    if logx:
        # Setup the logarithmic scale on the X axis
        data_array = np.array(data_list)
        vmin = np.log10(data_array.min())
        vmax = np.log10(data_array.max())
        bins = np.logspace(vmin, vmax, 50) # Make a range from 10**vmin to 10**vmax
    else:
        bins = 50

    if overlaid:
        for data_array, label in zip(data_list, label_list):
            res_tuple = axis.hist(data_array,
                                  bins=bins,
                                  log=logy,           # Set log scale on the Y axis
                                  histtype=HIST_TYPE,
                                  alpha=ALPHA,
                                  label=label)
    else:
        res_tuple = axis.hist(data_list,
                              bins=bins,
                              log=logy,               # Set log scale on the Y axis
                              histtype=HIST_TYPE,
                              alpha=ALPHA,
                              label=label_list)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--tight", action="store_true", default=False,
                        help="Optimize the X axis usage")

    parser.add_argument("--max", "-m", type=float, default=None, metavar="FLOAT", 
                        help="The maximum abscissa value to plot")

    parser.add_argument("--overlaid", "-O", action="store_true", default=False,
                        help="Overlaid histograms")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    logx = args.logx
    logy = args.logy
    tight = args.tight
    max_abscissa = args.max
    overlaid = args.overlaid
    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        prefix1 = "_o" if overlaid else ""
        prefix2 = "_" + str(max_abscissa) if max_abscissa is not None else ""
        output_file_path = "execution_time{}{}.pdf".format(prefix1, prefix2)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    data_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        json_dict = common.parse_json_file(json_file_path)

        execution_time_list = extract_execution_time_list(json_dict)

        if max_abscissa is not None:
            execution_time_list = [val for val in execution_time_list if val <= max_abscissa]

        data_list.append(np.array(execution_time_list))

        label_list.append(json_dict["label"])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    plot_hist(ax1, data_list, label_list, logx, logy, overlaid)

    ax1.axvline(x=0.00003, linewidth=1, color='gray', linestyle='dashed', label=r'30 $\mu$s')  # The maximum time allowed per event on CTA

    if tight:
        result_array = np.array(data_list)
        min_abscissa = result_array.min()
        max_abscissa = result_array.max()
        ax1.set_xlim(xmin=min_abscissa)
        ax1.set_xlim(xmax=max_abscissa)

    if max_abscissa is not None:
        ax1.set_xlim(xmax=max_abscissa)

    ax1.legend(prop={'size': 20})

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        ax1.set_title("Execution time", fontsize=20)

    ax1.set_xlabel("Execution time (seconds)", fontsize=20)
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

