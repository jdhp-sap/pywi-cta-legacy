#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Search inputs by score range (in score JSON files).
"""

import common_functions as common

import argparse
import json
import sys

import numpy as np


def extract_input_path_and_score_list(json_dict, score_index):
    io_list = json_dict["io"]
    json_data = [(image_dict["input_file_path"], float(image_dict["score"][score_index])) for image_dict in io_list if "score" in image_dict]
    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--best", "-b", type=int, default=None, metavar="INT",
                        help="Select the N best images")

    parser.add_argument("--worst", "-w", type=int, default=None, metavar="INT",
                        help="Select the N worst images")

    parser.add_argument("--min", "-m", type=float, default=None, metavar="FLOAT",
                        help="The lower bound of the selected range")

    parser.add_argument("--max", "-M", type=float, default=None, metavar="FLOAT",
                        help="The upper bound of the selected range")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT",
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    num_best = args.best
    num_worst = args.worst
    min_score = args.min
    max_score = args.max
    score_index = args.index
    json_file_path = args.fileargs[0]

    if (num_best is not None) and (num_worst is not None):
        raise Exception("--best and --worst options are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)
    data_list = extract_input_path_and_score_list(json_dict, score_index)

    # SEARCH INPUTS BY SCORE RANGE ############################################

    score_list = [item[1] for item in data_list]

    if min_score is None:
        min_score = min(score_list)

    if max_score is None:
        max_score = max(score_list)


    filtered_data_list = [item for item in data_list if ((item[1] >= min_score) and (item[1] <= max_score))]

    filtered_data_list = sorted(filtered_data_list, key=lambda item: item[1])


    if num_best is not None:
        filtered_data_list = filtered_data_list[:num_best]

    if num_worst is not None:
        filtered_data_list = filtered_data_list[-num_worst:]


    print("Min:", min_score, file=sys.stderr)
    print("Max:", max_score, file=sys.stderr)

    for file_path, score in filtered_data_list:
        #print(file_path)
        print(file_path, score)

    print(len(filtered_data_list), "inputs", file=sys.stderr)
