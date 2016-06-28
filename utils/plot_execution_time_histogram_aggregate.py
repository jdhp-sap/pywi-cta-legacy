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

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    json_file_path_list = args.fileargs

    # FETCH SCORE #############################################################

    result_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        score_dict = fetch_score(json_file_path)
        execution_time_list = score_dict["execution_time_list"]

        execution_time_array = np.array(execution_time_list)
        result_list.append(execution_time_array)

        # METADATA

        algo_path = score_dict["algo"]
        label_list.append(os.path.splitext(os.path.basename(algo_path))[0])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    res_tuple = ax1.hist(result_list, bins=50, histtype=HIST_TYPE, alpha=ALPHA, label=label_list)
    ax1.legend(prop={'size': 10})

    ax1.set_title("Execution time")
    ax1.set_xlabel("Execution time (seconds)")
    ax1.set_ylabel("Frequency")

    # Save file and plot ########

    output_file = "execution_time.pdf"

    plt.savefig(output_file)
    plt.show()

