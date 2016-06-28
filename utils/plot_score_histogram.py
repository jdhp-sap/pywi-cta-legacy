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


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    json_file_path = args.fileargs[0]

    # FETCH SCORE #############################################################

    score_dict = fetch_score(json_file_path)
    score_list = score_dict["score_list"]
    score_list = [score for score in score_list if not math.isnan(score)]

    score_array = np.array(score_list)

    # FETCH METADATA ##########################################################

    algo_path = score_dict["algo"]
    title = os.path.splitext(os.path.basename(algo_path))[0]

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    res_tuple = ax1.hist(score_array, bins=32, histtype=HIST_TYPE, alpha=ALPHA)
    ax1.set_title(title)
    ax1.set_xlabel("Score")
    ax1.set_ylabel("Frequency")

    # Save file and plot ########

    base_file_path = os.path.basename(json_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    output_file = base_file_path + ".pdf"

    plt.savefig(output_file)
    plt.show()

