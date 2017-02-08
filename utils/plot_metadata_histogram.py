#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5


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

    parser.add_argument("--key", "-k", required=True, metavar="STRING",
                        help='The key of the value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

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

    parser.add_argument("--output", "-o", default=None, metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None, metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    key = args.key
    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    tight = args.tight
    title = args.title
    quiet = args.quiet
    notebook = args.notebook
    json_file_path = args.fileargs[0]

    if args.output is None:
        base_file_path = os.path.basename(json_file_path)
        base_file_path = os.path.splitext(base_file_path)[0]
        output_file_path = "{}_{}.pdf".format(base_file_path, key)
    else:
        output_file_path = args.output

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)

    data_array = np.array(extract_data_list(json_dict, key, exclude_aborted, aborted_only))
    label = json_dict["label"]

    print("{} images".format(data_array.shape[0]))
    print("min:", data_array.min())
    print("max:", data_array.max())
    print("mean:", data_array.mean())

    # SET TITLE ###############################################################

    if title is None:
        if exclude_aborted:
            errors_str = "exclude errors"
        elif aborted_only:
            errors_str = "errors only"
        else:
            errors_str = None

        if errors_str is not None:
            title = "{} ({}) histogram for {}".format(key, errors_str, label)
        else:
            title = "{} histogram for {}".format(key, label)

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16, 9))

    common.plot_hist1d(ax1,
                       [data_array],
                       num_bins=50,
                       logx=logx,
                       logy=logy,
                       xlabel=key,
                       title=title,
                       tight=tight,
                       info_box_rms=False,
                       info_box_std=True,
                       plot_ratio=False)

    # SAVE FILE AND PLOT ######################################################

    if not notebook:
        plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

