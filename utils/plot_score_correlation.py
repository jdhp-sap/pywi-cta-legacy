#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
import numpy as np
from matplotlib import pyplot as plt

def fetch_data(json_file_path):
    with open(json_file_path, "r") as fd:
        score_dict = json.load(fd)
    return score_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

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

    parser.add_argument("--index1", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--index2", type=int, default=1, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    logx = args.logx
    logy = args.logy
    title = args.title
    quiet = args.quiet
    json_file_path = args.fileargs[0]

    score_index1 = args.index1
    score_index2 = args.index2

    # FETCH SCORE #############################################################

    score_dict = fetch_data(json_file_path)

    score_list = score_dict["score_list"]
    score_list = [[score[score_index1], score[score_index2]] for score in score_list]

    score_array = np.array(score_list)

    # METADATA

    try:
        label = score_dict["label"]
    except:
        algo_path = score_dict["algo"]
        label = os.path.splitext(os.path.basename(algo_path))[0]

    if args.output is None:
        suffix = label + "_i" + str(score_index1) + "_i" + str(score_index2)
        output_file_path = "score_correlation{}.pdf".format(suffix)
    else:
        output_file_path = args.output

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    ax1.plot(score_array[:,0], score_array[:,1], '.')

    ax1.legend(prop={'size': 20})

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        ax1.set_title("{} scores correlation".format(label), fontsize=20)

    ax1.set_xlabel("Score {}".format(score_index1), fontsize=20)
    ax1.set_ylabel("Score {}".format(score_index2), fontsize=20)

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


