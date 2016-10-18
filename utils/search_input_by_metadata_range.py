#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Search inputs by metadata range (in score JSON files).
"""

import common_functions as common

import argparse
import json
import sys

import numpy as np


def extract_input_path_and_meta_list(json_dict, key):
    io_list = json_dict["io"]
    json_data = [(image_dict["input_file_path"], image_dict[key], image_dict["score"]) for image_dict in io_list if "score" in image_dict]
    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--highest", "-H", type=int, default=None, metavar="INT",
                        help="Select the N images having the highest metadata value")

    parser.add_argument("--lowest", "-l", type=int, default=None, metavar="INT",
                        help="Select the N images having the lowest metadata value")

    parser.add_argument("--min", "-m", type=float, default=None, metavar="FLOAT",
                        help="The lower bound of the selected range")

    parser.add_argument("--max", "-M", type=float, default=None, metavar="FLOAT",
                        help="The upper bound of the selected range")

    parser.add_argument("--key", "-k", metavar="KEY",
                        help="The name of the metadata to considere")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    num_highest = args.highest
    num_lowest = args.lowest
    min_value = args.min
    max_value = args.max
    key = args.key
    json_file_path = args.fileargs[0]

    if (num_highest is not None) and (num_lowest is not None):
        raise Exception("--highest and --lowest options are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)
    data_list = extract_input_path_and_meta_list(json_dict, key)

    # SETUP RANGE #############################################################

    value_list = [item[1] for item in data_list]

    if min_value is None:
        min_value = min(value_list)

    if max_value is None:
        max_value = max(value_list)

    # SEARCH INPUTS BY SCORE RANGE ############################################

    filtered_data_list = [item for item in data_list if ((item[1] >= min_value) and (item[1] <= max_value))]

    filtered_data_list = sorted(filtered_data_list, key=lambda item: item[1])


    if num_highest is not None:
        filtered_data_list = filtered_data_list[-num_highest:]

    if num_lowest is not None:
        filtered_data_list = filtered_data_list[:num_lowest]


    print("Min:", min_value, file=sys.stderr)
    print("Max:", max_value, file=sys.stderr)

    for file_path, value, score in filtered_data_list:
        #print(file_path)
        print(file_path, value, score)

    print(len(filtered_data_list), "inputs", file=sys.stderr)

