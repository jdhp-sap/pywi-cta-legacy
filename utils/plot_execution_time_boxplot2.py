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


def extract_data_list(json_dict, key, exclude_aborted, aborted_only):
    io_list = json_dict["io"]

    if exclude_aborted:
        json_data = [image_dict[key] for image_dict in io_list if "error" not in image_dict]
    elif aborted_only:
        json_data = [image_dict[key] for image_dict in io_list if "error" in image_dict]
    else:
        json_data = [image_dict[key] for image_dict in io_list]

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

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        output_file_path = "execution_time_boxplot.png"
    else:
        output_file_path = args.output

    json_file_path = json_file_path_list[0]


    exclude_aborted = True
    aborted_only = False

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)

    data_list = []
    label_list = []

    key_list = ["load_input_image_time_sec",
                "full_clean_execution_time_sec",
                "load_tmp_file_time_sec",
                "mrfilter_cmd_exec_time_sec",
                "save_tmp_file_time_sec",
                "scipy_kill_isolated_pixels_time_sec"]

    for key in key_list:
        data_array = np.array(extract_data_list(json_dict, key, exclude_aborted, aborted_only))
        data_list.append(data_array)

        if key == "load_input_image_time_sec":
            label_list.append("load_in")
        elif key == "full_clean_execution_time_sec":
            label_list.append("clean")
        elif key == "load_tmp_file_time_sec":
            label_list.append("load_tmp")
        elif key == "mrfilter_cmd_exec_time_sec":
            label_list.append("mrfilter")
        elif key == "save_tmp_file_time_sec":
            label_list.append("save_tmp")
        elif key == "scipy_kill_isolated_pixels_time_sec":
            label_list.append("kill_pix")

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    whiskerprops = dict(color='k', linestyle='-')

    bp = ax1.boxplot(data_list,
                     labels=label_list,
                     meanprops=meanpointprops,
                     whiskerprops=whiskerprops,
                     #notch=True,
                     meanline=False,
                     showmeans=True)

    ax1.axhline(y=0.00003, linewidth=1, color='gray', linestyle='dashed', label=r'30 $\mu$s')  # The maximum time allowed per event on CTA

    ax1.set_yscale('log')

    ax1.legend(prop={'size': 18}, loc='upper left')

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        ax1.set_title("Execution time", fontsize=20)

    ax1.set_ylabel("Execution time (seconds)", fontsize=20)

    #plt.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=16)
    #plt.setp(ax1.get_xticklabels(), rotation=10, fontsize=16)
    plt.setp(ax1.get_xticklabels(), fontsize=16)
    plt.setp(ax1.get_yticklabels(), fontsize=16)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

