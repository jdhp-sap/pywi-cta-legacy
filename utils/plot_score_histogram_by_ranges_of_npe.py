#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
from matplotlib import pyplot as plt

import copy

NPE_RANGE_1 = (   0,      50)
NPE_RANGE_2 = (  50,     100)
NPE_RANGE_3 = ( 100,     110)
NPE_RANGE_4 = ( 110,    1000)
NPE_RANGE_5 = (1000, 1000000)

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

    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    title = args.title
    metric = args.metric
    tel_id = args.telid
    quiet = args.quiet
    notebook = args.notebook
    json_file_path_list = args.fileargs

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    if args.output is None:
        suffix  = "_" + metric
        suffix += "_tel{}".format(tel_id) if tel_id is not None else ""
        suffix += "_logx" if logx else ""
        suffix += "_logy" if logy else ""
        suffix += "_exclude-aborted" if exclude_aborted else ""
        suffix += "_aborted-only" if aborted_only else ""
        output_file_path = "score_histogram-x4{}.png".format(suffix)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    data_list1 = []
    data_list2 = []
    data_list3 = []
    data_list4 = []
    label_list = []

    for json_file_path in json_file_path_list:
        if not notebook:
            print("Parsing {}...".format(json_file_path))

        json_dict = common.parse_json_file(json_file_path)

        if tel_id is not None:
            json_dict = common.image_filter_equals(json_dict, "tel_id", tel_id)

        json_dict1 = common.image_filter_range(copy.deepcopy(json_dict), "npe", *NPE_RANGE_1)
        json_dict2 = common.image_filter_range(copy.deepcopy(json_dict), "npe", *NPE_RANGE_2)
        json_dict3 = common.image_filter_range(copy.deepcopy(json_dict), "npe", *NPE_RANGE_3)
        json_dict4 = common.image_filter_range(copy.deepcopy(json_dict), "npe", *NPE_RANGE_4)

        if not notebook:
            print(len(json_dict["io"]), "images")

        score_array1 = common.extract_score_array(json_dict1, metric)
        score_array2 = common.extract_score_array(json_dict2, metric)
        score_array3 = common.extract_score_array(json_dict3, metric)
        score_array4 = common.extract_score_array(json_dict4, metric)

        data_list1.append(score_array1)
        data_list2.append(score_array2)
        data_list3.append(score_array3)
        data_list4.append(score_array4)

        label_list.append(json_dict["label"])

    # PLOT STATISTICS #########################################################

    if not notebook:
        print("Plotting...")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 9))

    num_bins = 30
    legend_fontsize = 14
    show_info_box = True
    info_box_num_samples = True
    info_box_mean = False
    info_box_rms = False
    info_box_std = False

    common.plot_hist1d(axis=ax1,
                       data_list=data_list1,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       num_bins=num_bins,
                       legend_fontsize=legend_fontsize,
                       show_info_box=show_info_box,
                       info_box_num_samples=info_box_num_samples,
                       info_box_mean=info_box_mean,
                       info_box_rms=info_box_rms,
                       info_box_std=info_box_std)

    common.plot_hist1d(axis=ax2,
                       data_list=data_list2,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       num_bins=num_bins,
                       legend_fontsize=legend_fontsize,
                       show_info_box=show_info_box,
                       info_box_num_samples=info_box_num_samples,
                       info_box_mean=info_box_mean,
                       info_box_rms=info_box_rms,
                       info_box_std=info_box_std)

    common.plot_hist1d(axis=ax3,
                       data_list=data_list3,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       num_bins=num_bins,
                       legend_fontsize=legend_fontsize,
                       show_info_box=show_info_box,
                       info_box_num_samples=info_box_num_samples,
                       info_box_mean=info_box_mean,
                       info_box_rms=info_box_rms,
                       info_box_std=info_box_std)

    common.plot_hist1d(axis=ax4,
                       data_list=data_list4,
                       label_list=label_list,
                       logx=logx,
                       logy=logy,
                       num_bins=num_bins,
                       legend_fontsize=legend_fontsize,
                       show_info_box=show_info_box,
                       info_box_num_samples=info_box_num_samples,
                       info_box_mean=info_box_mean,
                       info_box_rms=info_box_rms,
                       info_box_std=info_box_std)

    ax1.set_title("{} to {} NPE".format(*NPE_RANGE_1), fontsize=20)
    ax2.set_title("{} to {} NPE".format(*NPE_RANGE_2), fontsize=20)
    ax3.set_title("{} to {} NPE".format(*NPE_RANGE_3), fontsize=20)
    ax4.set_title("{} to {} NPE".format(*NPE_RANGE_4), fontsize=20)
    
    if title is not None:
        plt.suptitle(title, fontsize=20)
    else:
        plt.suptitle(metric, fontsize=20)
#    else:
#        if exclude_aborted:
#            errors_str = "exclude errors"
#        elif aborted_only:
#            errors_str = "errors only"
#        else:
#            errors_str = None
#
#        if errors_str is not None:
#            ax1.set_title("{} - {} correlation ({})".format(key1, key2, errors_str), fontsize=20)
#        else:
#            ax1.set_title("{} - {} correlation".format(key1, key2), fontsize=20)

    # Save file and plot ########

    if not notebook:
        plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

