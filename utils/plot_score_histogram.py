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


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--tight", action="store_true", default=False,
                        help="Optimize the X axis usage")

    parser.add_argument("--max", type=float, default=None, metavar="FLOAT", 
                        help="The maximum abscissa value to plot")

    parser.add_argument("--metric", "-m", required=True,
                        metavar="STRING",
                        help="The metric name to plot")

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
    metric = args.metric
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        suffix1 = "_" + metric
        suffix2 = "_o" if overlaid else ""
        suffix3 = "_" + str(max_abscissa) if max_abscissa is not None else ""
        output_file_path = "scores{}{}{}.pdf".format(suffix1, suffix2, suffix3)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    data_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        print("Parsing {}...".format(json_file_path))

        json_dict = common.parse_json_file(json_file_path)

        print(len(json_dict["io"]), "images")

        score_array = common.extract_score_array(json_dict, metric)

        if max_abscissa is not None:
            score_array = np.array([score for score in score_array if score <= max_abscissa])

        data_list.append(score_array)

        label_list.append(json_dict["label"])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    common.plot_hist1d(ax1,
                       data_list,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       xmax=max_abscissa,
                       overlaid=overlaid,
                       xlabel="Score",
                       title=title,
                       num_bins=30,
                       tight=tight)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

