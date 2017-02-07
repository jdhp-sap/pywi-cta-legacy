#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--exclude-aborted", action="store_true", default=False,
                        help="Ignore values from aborted images")

    parser.add_argument("--aborted-only", action="store_true", default=False,
                        help="Only consider aborted images")

    parser.add_argument("--logx", "-l", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", "-L", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--tight", action="store_true", default=False,
                        help="Optimize the X axis usage")

    parser.add_argument("--min-score", type=float, default=None, metavar="FLOAT", 
                        help="The minimum abscissa value to plot")

    parser.add_argument("--max-score", type=float, default=None, metavar="FLOAT", 
                        help="The maximum abscissa value to plot")

    parser.add_argument("--min-npe", type=float, default=None, metavar="FLOAT", 
                        help="Only considere images having more than the specified total number of photo electrons")

    parser.add_argument("--max-npe", type=float, default=None, metavar="FLOAT", 
                        help="Only considere images having less than the specified total number of photo electrons")

    parser.add_argument("--metric", "-m", required=True,
                        metavar="STRING",
                        help="The metric name to plot")

    parser.add_argument("--overlaid", "-O", action="store_true", default=False,
                        help="Overlaid histograms")

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

    parser.add_argument("--ratio", action="store_true", default=False,
                        help="Plot the ratio of the first input file to the second one (require exactly 2 input files)")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("--degx", action="store_true",
                        help="Make bins in degrees")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    tight = args.tight
    min_abscissa = args.min_score
    max_abscissa = args.max_score
    min_npe = args.min_npe
    max_npe = args.max_npe
    metric = args.metric
    overlaid = args.overlaid
    title = args.title
    tel_id = args.telid
    quiet = args.quiet
    plot_ratio = args.ratio
    notebook = args.notebook
    degx = args.degx
    json_file_path_list = args.fileargs

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    if args.output is None:
        suffix  = "_" + metric
        suffix += "_tel{}".format(tel_id) if tel_id is not None else ""
        suffix += "_logx" if logx else ""
        suffix += "_logy" if logy else ""
        suffix += "_min{}".format(min_abscissa) if min_abscissa is not None else ""
        suffix += "_max{}".format(max_abscissa) if max_abscissa is not None else ""
        suffix += "_min-npe{}".format(min_npe) if min_npe is not None else ""
        suffix += "_max-npe{}".format(max_npe) if max_npe is not None else ""
        suffix += "_exclude-aborted" if exclude_aborted else ""
        suffix += "_aborted-only" if aborted_only else ""
        output_file_path = "score_histogram{}.png".format(suffix)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    data_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        if not notebook:
            print("Parsing {}...".format(json_file_path))

        json_dict = common.parse_json_file(json_file_path)

        if tel_id is not None:
            json_dict = common.image_filter_equals(json_dict, "tel_id", tel_id)

        if min_npe is not None:
            json_dict = common.image_filter_range(json_dict, "npe", min_value=min_npe)

        if max_npe is not None:
            json_dict = common.image_filter_range(json_dict, "npe", max_value=max_npe)

        if not notebook:
            print(len(json_dict["io"]), "images")

        score_array = common.extract_score_array(json_dict, metric)

        if min_abscissa is not None:
            score_array = np.array([score for score in score_array if score >= min_abscissa])

        if max_abscissa is not None:
            score_array = np.array([score for score in score_array if score <= max_abscissa])

        data_list.append(score_array)

        label_list.append(json_dict["label"])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))

    common.plot_hist1d(ax1,
                       data_list,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       xmax=max_abscissa,
                       overlaid=overlaid,
                       xlabel="Score",
                       title=title,
                       num_bins=30,
                       #num_bins=[0., 0.0011, 0.0022, 0.0033],
                       tight=tight,
                       plot_ratio=plot_ratio,
                       degx=degx)

    # Save file and plot ########

    if not notebook:
        plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

