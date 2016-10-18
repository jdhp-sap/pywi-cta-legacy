#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import matplotlib.pyplot as plt


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--key", "-k", required=True, metavar="STRING",
                        help='The key of the value to plot (e.g. "mc_energy" or "npe")')

    parser.add_argument("--logx", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--logz", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    key = args.key
    logx = args.logx
    logy = args.logy
    logz = args.logz
    score_index = args.index
    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        output_file_path = "scores2d_i{}.pdf".format(score_index)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    score_array_list = []
    metadata_array_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        json_dict = common.parse_json_file(json_file_path)

        score_array = common.extract_score_array(json_dict, score_index)
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

        common.plot_hist2d(axis, score_array, metadata_array, logx, logy, logz, xmin, xmax, ymin, ymax, zmin=None, zmax=None)

        axis.legend(prop={'size': 20})

        # Sub titles
        axis.set_title(label, fontsize=20)

        axis.set_xlabel("score", fontsize=20)
        axis.set_ylabel(key, fontsize=20)

        plt.setp(axis.get_xticklabels(), fontsize=14)
        plt.setp(axis.get_yticklabels(), fontsize=14)


    # Main title
    if title is not None:
        fig.suptitle(title, fontsize=20)
    else:
        suffix = " (index {})".format(score_index)
        fig.suptitle("Score" + suffix, fontsize=20)

    plt.subplots_adjust(top=0.85)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

