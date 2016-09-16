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


def fetch_data(json_file_path):

    with open(json_file_path, "r") as fd:
        score_dict = json.load(fd)

    return score_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    json_file_path_list = args.fileargs

    score_index = args.index

    if args.output is None:
        suffix = "_i" + str(score_index)
        output_file_path = "score_boxplot{}.pdf".format(suffix)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    result_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        score_dict = fetch_data(json_file_path)
        score_list = score_dict["score_list"]

        score_list = [score[score_index] for score in score_list] # TODO...
        score_list = [score for score in score_list if not math.isnan(score)]

        score_array = np.array(score_list)
        result_list.append(score_array)

        # METADATA
        try:
            label_list.append(score_dict["label"])
        except:
            algo_path = score_dict["algo"]
            label_list.append(os.path.splitext(os.path.basename(algo_path))[0])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    whiskerprops = dict(color='k', linestyle='-')

    bp = ax1.boxplot(result_list,
                     labels=label_list,
                     meanprops=meanpointprops,
                     whiskerprops=whiskerprops,
                     #notch=True,
                     meanline=False,
                     showmeans=True)

    ax1.set_yscale('log')

    ax1.legend(prop={'size': 18}, loc='upper left')

    suffix = " (index {})".format(score_index)
    ax1.set_title("Score" + suffix, fontsize=20)
    ax1.set_ylabel("Score", fontsize=20)

    #plt.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=16)
    #plt.setp(ax1.get_xticklabels(), rotation=10, fontsize=16)
    plt.setp(ax1.get_xticklabels(), fontsize=16)
    plt.setp(ax1.get_yticklabels(), fontsize=16)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')
    plt.show()

