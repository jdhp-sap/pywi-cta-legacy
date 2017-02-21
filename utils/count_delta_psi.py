#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

# To ignore warnings (http://stackoverflow.com/questions/9031783/hide-all-warnings-in-ipython)
import warnings
warnings.filterwarnings('ignore')

import common_functions as common

import argparse
import numpy as np

def count_delta_psi(json_file_path,
                    min_npe=None,
                    max_npe=None,
                    notebook=False,
                    delta_angle_degrees=0.05,
                    border=False):

    # FETCH SCORE AND COMPUTE HISTOGRAM #######################################

    json_dict = common.parse_json_file(json_file_path)

    if min_npe is not None:
        json_dict = common.image_filter_range(json_dict, "img_cleaned_sum_pe", min_value=min_npe)

    if max_npe is not None:
        json_dict = common.image_filter_range(json_dict, "img_cleaned_sum_pe", max_value=max_npe)

    if border:
        json_dict = common.image_filter_range(json_dict, "img_cleaned_signal_to_border_distance", min_value=1)

    score_array = common.extract_score_array(json_dict, "hillas2_delta_psi_norm2")

    score_array = np.abs(score_array)
    count = len(score_array[score_array < delta_angle_degrees])

    return count


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--border", action="store_true", default=False,
                        help="Ignore images where the shower is on one border")

    parser.add_argument("--angle", type=float, default=None, metavar="FLOAT",
                        help="Delta angle (in degrees) of the first bin")

    parser.add_argument("--min-npe", type=float, default=None, metavar="FLOAT",
                        help="Only considere images having more than the specified total number of photo electrons")

    parser.add_argument("--max-npe", type=float, default=None, metavar="FLOAT",
                        help="Only considere images having less than the specified total number of photo electrons")

    parser.add_argument("--notebook", action="store_true",
                        help="Notebook mode")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    border = args.border
    angle = args.angle
    min_npe = args.min_npe
    max_npe = args.max_npe
    notebook = args.notebook
    json_file_path = args.fileargs[0]

    count = count_delta_psi(json_file_path,
                            min_npe=min_npe,
                            max_npe=max_npe,
                            notebook=notebook,
                            delta_angle_degrees=angle,
                            border=border)

    print(count)

