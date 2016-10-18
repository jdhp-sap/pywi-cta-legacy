#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import json
import numpy as np


def extract_data_list(json_dict):
    io_list = json_dict["io"]

    success_list = [image_dict for image_dict in io_list if "error" not in image_dict]
    aborted_list = [image_dict for image_dict in io_list if "error" in image_dict]

    return success_list, aborted_list


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    json_file_path = args.fileargs[0]

    # FETCH SCORE #############################################################

    json_data = common.parse_json_file(json_file_path)

    success_list, aborted_list = extract_data_list(json_data)

    print("{} images".format(len(success_list) + len(aborted_list)))
    print("{} succeeded".format(len(success_list)))
    print("{} failed".format(len(aborted_list)))

    if len(aborted_list) > 0:
        error_message_dict = {}
        for image_dict in aborted_list:
            error_message = image_dict["error"]["message"]
            if error_message in error_message_dict:
                error_message_dict[error_message] += 1
            else:
                error_message_dict[error_message] = 1

        for error_message, count in error_message_dict.items():
            print("-> {}: {}".format(error_message, count))
