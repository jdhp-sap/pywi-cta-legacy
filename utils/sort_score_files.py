#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import json
import math
import numpy as np
import operator

def extract_score_list(json_dict, score_index):
    io_list = json_dict["io"]
    json_data = [image_dict["score"][score_index] for image_dict in io_list if "score" in image_dict]
    return json_data


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    json_file_path_list = args.fileargs
    score_index = args.index


    # FETCH SCORE #############################################################

    data_dict = {}
    error_list = []

    for json_file_path in json_file_path_list:
        try:
            json_dict = common.parse_json_file(json_file_path)
            score_array = np.array(extract_score_list(json_dict, score_index))
            mean_score = score_array.mean()
            if math.isnan(mean_score):
                error_list.append(json_file_path)
            else:
                data_dict[json_file_path] = mean_score
        except: 
            error_list.append(json_file_path)

    print("ERRORS")
    for path in error_list:
        print(path)

    print("")
    print("SORTED SCORES")
    for path, mean in sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True):
        print(mean, path)

