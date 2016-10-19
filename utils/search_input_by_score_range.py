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


def extract_input_path_with_score_and_meta_list(json_dict, score_index, meta_key=None):
    io_list = json_dict["io"]

    if meta_key is None:
        json_data = [(image_dict["input_file_path"], float(image_dict["score"][score_index])) for image_dict in io_list if "score" in image_dict]
    else:
        json_data = [(image_dict["input_file_path"], float(image_dict["score"][score_index], image_dict[meta_key])) for image_dict in io_list if "score" in image_dict]

    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--num-best-scores", "-b", type=int, default=None, metavar="INT",
                        help="Select the N best images")

    parser.add_argument("--num-worst-scores", "-w", type=int, default=None, metavar="INT",
                        help="Select the N worst images")

    parser.add_argument("--min-score", "-m", type=float, default=None, metavar="FLOAT",
                        help="The lower bound of the selected range")

    parser.add_argument("--max-score", "-M", type=float, default=None, metavar="FLOAT",
                        help="The upper bound of the selected range")

    parser.add_argument("--score-index", "-i", type=int, default=0, metavar="INT",
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--metadata-key", "-k", metavar="KEY",
                        help="The name of the metadata to filter")

    parser.add_argument("--min-key-value", type=float, default=None, metavar="FLOAT",
                        help="The lower bound of the selected range")

    parser.add_argument("--max-key-value", type=float, default=None, metavar="FLOAT",
                        help="The upper bound of the selected range")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    num_best_scores = args.num_best_scores
    num_worst_scores = args.num_worst_scores
    min_score = args.min_score
    max_score = args.max_score
    score_index = args.score_index
    metadata_key = args.metadata_key
    min_key_value = args.min_key_value
    max_key_value = args.max_key_value
    json_file_path = args.fileargs[0]

    if (num_best_scores is not None) and (num_worst_scores is not None):
        raise Exception("--best and --worst options are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)
    data_list = extract_input_path_with_score_and_meta_list(json_dict, score_index, metadata_key)

    # SETUP SCORE RANGE #######################################################

    score_list = [item[1] for item in data_list]

    if min_score is None:
        min_score = min(score_list)

    if max_score is None:
        max_score = max(score_list)

    # SETUP METADATA RANGE ####################################################

    if metadata_key is not None:
        metadata_value_list = [item[2] for item in data_list]

        if min_key_value is None:
            min_key_value = min(metadata_value_list)

        if max_key_value is None:
            max_key_value = max(metadata_value_list)

    # SEARCH INPUTS BY SCORE RANGE ############################################

    if metadata_key is None:
        filtered_data_list = [item for item in data_list if ((item[1] >= min_score) and (item[1] <= max_score))]
    else:
        filtered_data_list = [item for item in data_list if ((item[1] >= min_score) and (item[1] <= max_score) and (item[2] >= min_key_value) and (item[2] <= max_key_value))]

    filtered_data_list = sorted(filtered_data_list, key=lambda item: item[1], reverse=True)


    if num_best_scores is not None:
        filtered_data_list = filtered_data_list[-num_best_scores:]

    if num_worst_scores is not None:
        filtered_data_list = filtered_data_list[:num_worst_scores]


    print("Min:", min_score, file=sys.stderr)
    print("Max:", max_score, file=sys.stderr)

    if metadata_key is None:
        for file_path, score in filtered_data_list:
            #print(file_path)
            print(file_path, score)
    else:
        for file_path, score, meta_value in filtered_data_list:
            #print(file_path)
            print(file_path, score, meta_value)

    print(len(filtered_data_list), "inputs", file=sys.stderr)

