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

    parser.add_argument("--max", "-m", type=float, default=None, metavar="FLOAT", 
                        help="The maximum abscissa value to plot")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

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
    max_abscissa = args.max
    score_index = args.index
    overlaid = args.overlaid
    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        suffix1 = "_i" + str(score_index)
        suffix2 = "_o" if overlaid else ""
        suffix3 = "_" + str(max_abscissa) if max_abscissa is not None else ""
        output_file_path = "scores{}{}{}.pdf".format(suffix1, suffix2, suffix3)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    result_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        score_dict = fetch_score(json_file_path)
        score_list = score_dict["score_list"]

        score_list = [score[score_index] for score in score_list] # TODO...
        score_list = [score for score in score_list if not math.isnan(score)] # TODO...

        if max_abscissa is not None:
            score_list = [score for score in score_list if score <= max_abscissa]

        score_array = np.array(score_list)
        result_list.append(score_array)

        # METADATA
        try:
            label_list.append(score_dict["label"])
        except:
            algo_path = score_dict["algo"]
            label_list.append(os.path.splitext(os.path.basename(algo_path))[0])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    plot_hist(ax1, result_list, label_list, logx, logy, overlaid)

    if max_abscissa is not None:
        ax1.set_xlim(xmax=max_abscissa)

    ax1.legend(prop={'size': 20})

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        suffix = " (index {})".format(score_index)
        ax1.set_title("Score" + suffix, fontsize=20)

    ax1.set_xlabel("Score", fontsize=20)
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

