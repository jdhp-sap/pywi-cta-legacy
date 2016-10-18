#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import json
import numpy as np
from matplotlib import pyplot as plt


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--logz", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--index1", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--index2", type=int, default=1, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--hist2d", action="store_true",
                        help="Display an histogram")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    logx = args.logx
    logy = args.logy
    logz = args.logz
    title = args.title
    hist2d = args.hist2d
    quiet = args.quiet
    json_file_path = args.fileargs[0]

    score_index1 = args.index1
    score_index2 = args.index2

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)

    score_array = common.extract_score_2d_array(json_dict, score_index1, score_index2)

    label = json_dict["label"]

    if args.output is None:
        suffix = label + "_i" + str(score_index1) + "_i" + str(score_index2)
        output_file_path = "score_correlation{}.pdf".format(suffix)
    else:
        output_file_path = args.output

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    if hist2d:
        common.plot_hist2d(ax1,
                           score_array[:,0],
                           score_array[:,1],
                           "Score {}".format(score_index1),
                           "Score {}".format(score_index2),
                           logx,
                           logy,
                           logz)
    else:
        common.plot_correlation(ax1,
                                score_array[:,0],
                                score_array[:,1],
                                "Score {}".format(score_index1),
                                "Score {}".format(score_index2),
                                logx,
                                logy)

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        ax1.set_title("{} scores correlation".format(label), fontsize=20)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()


