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


def extract_score_list(json_dict, score_index):
    io_list = json_dict["io"]
    json_data = [image_dict["score"][score_index] for image_dict in io_list if "score" in image_dict]
    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    score_index = args.index

    if args.output is None:
        suffix = "_i" + str(score_index)
        output_file_path = "score_boxplot{}.pdf".format(suffix)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    data_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        json_dict = common.parse_json_file(json_file_path)

        score_array = np.array(extract_score_list(json_dict, score_index))
        data_list.append(score_array)

        label_list.append(json_dict["label"])


    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    whiskerprops = dict(color='k', linestyle='-')

    bp = ax1.boxplot(data_list,
                     labels=label_list,
                     meanprops=meanpointprops,
                     whiskerprops=whiskerprops,
                     #notch=True,
                     meanline=False,
                     showmeans=True)

    ax1.set_yscale('log')

    ax1.legend(prop={'size': 18}, loc='upper left')

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        suffix = " (index {})".format(score_index)
        ax1.set_title("Score" + suffix, fontsize=20)

    ax1.set_ylabel("Score", fontsize=20)

    #plt.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=16)
    #plt.setp(ax1.get_xticklabels(), rotation=10, fontsize=16)
    plt.setp(ax1.get_xticklabels(), fontsize=16)
    plt.setp(ax1.get_yticklabels(), fontsize=16)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

