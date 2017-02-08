#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import matplotlib.pyplot as plt

import copy

if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--key", "-k", required=True, metavar="STRING",
                        help='The key of the value to plot (e.g. "mc_energy" or "npe")')

    parser.add_argument("--key-min", type=float, default=None, metavar="FLOAT",
                        help='The key\'s minimum value to plot')

    parser.add_argument("--key-max", type=float, default=None, metavar="FLOAT",
                        help='The key\'s maximum value to plot')

    parser.add_argument("--logx", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--logz", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--metric", "-m", required=True,
                        metavar="STRING",
                        help="The metric name to plot")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--telid", type=int, default=None,
                        metavar="INTEGER",
                        help="Only plot results for this telescope")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    key = args.key
    key_min = args.key_min
    key_max = args.key_max
    logx = args.logx
    logy = args.logy
    logz = args.logz
    metric = args.metric
    title = args.title
    tel_id = args.telid
    quiet = args.quiet
    notebook = args.notebook
    json_file_path_list = args.fileargs

    if args.output is None:
        output_file_path = "scores2d_{}.png".format(metric)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    score_array_list = []
    metadata_array_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        if not notebook:
            print("Parsing {}...".format(json_file_path))

        json_dict = common.parse_json_file(json_file_path)

        if tel_id is not None:
            json_dict = common.image_filter_equals(json_dict, "tel_id", tel_id)

        if key_min is not None and key_max is not None:
            json_dict = common.image_filter_range(copy.deepcopy(json_dict), key, key_min, key_max)

        if not notebook:
            print(len(json_dict["io"]), "images")

        score_array = common.extract_score_array(json_dict, metric)
        score_array_list.append(score_array)

        metadata_array = common.extract_metadata_array(json_dict, key)
        metadata_array_list.append(metadata_array)

        label_list.append(json_dict["label"])

    xmin = common.extract_min(score_array_list)
    xmax = common.extract_max(score_array_list)
    ymin = common.extract_min(metadata_array_list)
    ymax = common.extract_max(metadata_array_list)

    # PLOT STATISTICS #########################################################

    fig, axis_array = plt.subplots(nrows=1, ncols=len(json_file_path_list), squeeze=False, figsize=(6 * len(json_file_path_list), 6))

    axis_array = axis_array.flat

    for (axis, score_array, metadata_array, label) in zip(axis_array, score_array_list, metadata_array_list, label_list):

        common.plot_hist2d(axis,
                           score_array,
                           metadata_array,
                           "Score",          # "Score (the lower the better)",
                           "Total counts in refernce image (PE)" if key == "npe" else key,
                           logx,
                           logy,
                           logz,
                           xmin,
                           xmax,
                           ymin,
                           ymax,
                           zmin=None,
                           zmax=None)

        # Sub titles
        axis.set_title(label, fontsize=20)


    # Main title
    if title is not None:
        fig.suptitle(title, fontsize=20)
    else:
        suffix = " ({})".format(metric)
        if key_min is not None and key_max is not None:
            suffix += " from {} to {} {}".format(key_min, key_max, key)
        if tel_id is not None:
            suffix += " Tel {}".format(tel_id)
        fig.suptitle("Score" + suffix, fontsize=20)

    plt.subplots_adjust(top=0.85)

    # Save file and plot ########

    if not notebook:
        plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

