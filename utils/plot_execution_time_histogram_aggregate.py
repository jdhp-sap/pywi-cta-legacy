#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
import math
import os

import matplotlib.pyplot as plt
import numpy as np

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5

def fetch_score(json_file_path):

    with open(json_file_path, "r") as fd:
        score_dict = json.load(fd)

    return score_dict


def plot_hist(axis, result_list, label_list):
    res_tuple = axis.hist(result_list, bins=50, histtype=HIST_TYPE, alpha=ALPHA, label=label_list)


def plot_overlaid_hist(axis, result_list, label_list):
    for result_array, label in zip(result_list, label_list):
        res_tuple = axis.hist(result_array, bins=50, histtype=HIST_TYPE, alpha=ALPHA, label=label)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--max", "-m", type=float, default=None, metavar="FLOAT", 
                        help="The maximum abscissa value to plot")
    parser.add_argument("--overlaid", "-O", action="store_true", default=False,
                        help="Overlaid histograms")
    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    max_abscissa = args.max
    overlaid = args.overlaid
    json_file_path_list = args.fileargs

    # FETCH SCORE #############################################################

    result_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        score_dict = fetch_score(json_file_path)
        execution_time_list = score_dict["execution_time_list"]

        if max_abscissa is not None:
            execution_time_list = [val for val in execution_time_list if val <= max_abscissa]

        execution_time_array = np.array(execution_time_list)
        result_list.append(execution_time_array)

        # METADATA

        algo_path = score_dict["algo"]
        label_list.append(os.path.splitext(os.path.basename(algo_path))[0])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    if overlaid:
        plot_overlaid_hist(ax1, result_list, label_list)
    else:
        plot_hist(ax1, result_list, label_list)

    ax1.axvline(x=0.00003, linewidth=1, color='gray', linestyle='dashed', label=r'$30 \mu s$')  # The maximum time allowed per event on CTA

    if max_abscissa is not None:
        ax1.set_xlim(xmax=max_abscissa)

    ax1.legend(prop={'size': 20})

    ax1.set_title("Execution time", fontsize=20)
    ax1.set_xlabel("Execution time (seconds)", fontsize=20)
    ax1.set_ylabel("Occurrences", fontsize=20)

    plt.setp(ax1.get_xticklabels(), fontsize=12)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    # Save file and plot ########

    prefix1 = "_o" if overlaid else ""
    prefix2 = "_" + str(max_abscissa) if max_abscissa is not None else ""
    output_file = "execution_time{}{}.pdf".format(prefix1, prefix2)

    plt.savefig(output_file, bbox_inches='tight')
    plt.show()

