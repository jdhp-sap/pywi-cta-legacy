#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
from matplotlib import pyplot as plt
import os


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

    parser.add_argument("--logz", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--key1", metavar="KEY", 
                        help='The key of the first value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

    parser.add_argument("--key2", metavar="KEY", 
                        help='The key of the second value to plot (e.g. "mc_energy", "npe", "telescope_id", ...)')

    parser.add_argument("--hist2d", action="store_true",
                        help="Display an histogram")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    logx = args.logx
    logy = args.logy
    logz = args.logz
    title = args.title
    hist2d = args.hist2d
    quiet = args.quiet
    json_file_path = args.fileargs[0]

    key1 = args.key1
    key2 = args.key2

    if args.output is None:
        base_file_path = os.path.basename(json_file_path)
        base_file_path = os.path.splitext(base_file_path)[0]
        output_file_path = "metadata_correlation_{}_{}_{}.pdf".format(base_file_path, key1, key2)
    else:
        output_file_path = args.output

    if exclude_aborted and aborted_only:
        raise Exception("--exclude-aborted and --aborted-only are not compatible")

    # FETCH SCORE #############################################################

    json_dict = common.parse_json_file(json_file_path)

    metadata_array = common.extract_metadata_2d_array(json_dict, key1, key2, exclude_aborted, aborted_only)
    label = json_dict["label"]

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    if hist2d:
        common.plot_hist2d(ax1,
                           metadata_array[:,0],
                           metadata_array[:,1],
                           key1,
                           key2,
                           logx,
                           logy,
                           logz)
    else:
        common.plot_correlation(ax1,
                                metadata_array[:,0],
                                metadata_array[:,1],
                                key1,
                                key2,
                                logx,
                                logy)

    if title is not None:
        ax1.set_title(title, fontsize=20)
    else:
        if exclude_aborted:
            errors_str = "exclude errors"
        elif aborted_only:
            errors_str = "errors only"
        else:
            errors_str = None

        if errors_str is not None:
            ax1.set_title("{} - {} correlation ({})".format(key1, key2, errors_str), fontsize=20)
        else:
            ax1.set_title("{} - {} correlation".format(key1, key2), fontsize=20)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()


