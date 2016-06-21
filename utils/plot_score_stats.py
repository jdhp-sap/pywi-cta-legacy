#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
import math

import matplotlib.pyplot as plt
import numpy as np

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

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    whiskerprops = dict(color='k', linestyle='-')
    bp = ax1.boxplot(score_array,
                     meanprops=meanpointprops,
                     whiskerprops=whiskerprops,
                     #notch=True,
                     meanline=False,
                     showmeans=True)
    #plt.setp(bp['whiskers'], color='k', linestyle='-')

    # Save file and plot ########

    #plt.savefig("stats.pdf")
    plt.show()

