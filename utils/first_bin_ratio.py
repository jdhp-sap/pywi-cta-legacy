#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import common_functions as common

import argparse
import numpy as np
import math

def hist_ratio(json_file_path_list,
               metric,
               min_npe=None,
               max_npe=None,
               exclude_aborted=False,
               aborted_only=False,
               tel_id=None,
               notebook=False,
               delta_angle_degrees=0.2):

    if len(json_file_path_list) != 2:
        raise Exception('"json_file_path_list" should have exactly 2 elements')

    if exclude_aborted and aborted_only:
        raise Exception('"exclude-aborted" and "aborted-only" options are not compatible"')

    # FETCH SCORE AND COMPUTE HISTOGRAM #######################################

    data_list = []
    label_list = []
    hist_list = []
    bins_list = []

    for json_file_path in json_file_path_list:
        if not notebook:
            print("Parsing {}...".format(json_file_path))

        json_dict = common.parse_json_file(json_file_path)

        if tel_id is not None:
            json_dict = common.image_filter_equals(json_dict, "tel_id", tel_id)

        if min_npe is not None:
            #json_dict = common.image_filter_range(json_dict, "npe", min_value=min_npe)
            json_dict = common.image_filter_range(json_dict, "img_cleaned_sum_pe", min_value=min_npe)

        if max_npe is not None:
            #json_dict = common.image_filter_range(json_dict, "npe", max_value=max_npe)
            json_dict = common.image_filter_range(json_dict, "img_cleaned_sum_pe", max_value=max_npe)

        if not notebook:
            print(len(json_dict["io"]), "images")

        score_array = common.extract_score_array(json_dict, metric)

        data_list.append(score_array)

        label_list.append(json_dict["label"])

        min_range, max_range = 0., math.sin(math.radians(delta_angle_degrees))

        hist, bin_edges = np.histogram(score_array,
                                       range=(min_range, max_range),
                                       bins=1)
                                       #bins=[0., math.sin(math.radians(0.2)), math.sin(math.radians(0.4)), math.sin(math.radians(0.6))] )

        hist_list.append(hist)
        bins_list.append(bin_edges)

    # COMPUTE RATIO ###########################################################

    #assert bins_list[0] == bins_list[1]

    edges_of_bins = bins_list[0]
    val_of_bins_data_1 = hist_list[0]
    val_of_bins_data_2 = hist_list[1]

    print(val_of_bins_data_1)
    print(val_of_bins_data_2)

    # Set ratio where val_of_bins_data_2 is not zero
    ratio = np.divide(val_of_bins_data_1,
                      val_of_bins_data_2,
                      where=(val_of_bins_data_2 != 0))

    # Compute error on ratio (null if cannot be computed)
    error = np.divide(val_of_bins_data_1 * np.sqrt(val_of_bins_data_2) + val_of_bins_data_2 * np.sqrt(val_of_bins_data_1),
                      np.power(val_of_bins_data_2, 2),
                      where=(val_of_bins_data_2 != 0))

    return ratio, error, edges_of_bins


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--exclude-aborted", action="store_true", default=False,
                        help="Ignore values from aborted images")

    parser.add_argument("--aborted-only", action="store_true", default=False,
                        help="Only consider aborted images")

    parser.add_argument("--angle", type=float, default=None, metavar="FLOAT", 
                        help="Delta angle (in degrees) of the first bin")

    parser.add_argument("--min-npe", type=float, default=None, metavar="FLOAT", 
                        help="Only considere images having more than the specified total number of photo electrons")

    parser.add_argument("--max-npe", type=float, default=None, metavar="FLOAT", 
                        help="Only considere images having less than the specified total number of photo electrons")

    parser.add_argument("--metric", "-m", required=True,
                        metavar="STRING",
                        help="The metric name to plot")

    parser.add_argument("--telid", type=int, default=None,
                        metavar="INTEGER",
                        help="Only plot results for this telescope")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("fileargs", nargs=2, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    exclude_aborted = args.exclude_aborted
    aborted_only = args.aborted_only
    angle = args.angle
    min_npe = args.min_npe
    max_npe = args.max_npe
    metric = args.metric
    tel_id = args.telid
    notebook = args.notebook
    json_file_path_list = args.fileargs

    ratio, error, bins = hist_ratio(json_file_path_list,
                                    metric,
                                    min_npe=min_npe,
                                    max_npe=max_npe,
                                    exclude_aborted=exclude_aborted,
                                    aborted_only=aborted_only,
                                    tel_id=tel_id,
                                    notebook=notebook,
                                    delta_angle_degrees=angle)

    print("ratio:", ratio)
    print("error:", error)
    print("bins:", bins)

