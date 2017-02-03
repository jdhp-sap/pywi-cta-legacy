#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import common_functions as common

import argparse
import collections
import numpy as np
import math


COLUMNS_DESC = collections.OrderedDict()
COLUMNS_DESC["Part"]    = "Particle, 0:gamma, -1:electron/positron, 1:proton (iron would be 26)"
COLUMNS_DESC["Id"]      = "A string built like this : event#_telescope#, see below (e.g telescope 1 and event 84 gives 84_1)"
COLUMNS_DESC["Evt"]     = "Event ID"
COLUMNS_DESC["Tel"]     = "Telescope ID"
COLUMNS_DESC["Exect"]   = "Execution time (in second)"
COLUMNS_DESC["Xtel"]    = "x coordinates of telescope (in meter)"
COLUMNS_DESC["Ytel"]    = "y coordinates of telescope (in meter)"
COLUMNS_DESC["Ztel"]    = "z coordinates of telescope (in meter)"
COLUMNS_DESC["E"]       = "Event energy (in TeV)"
COLUMNS_DESC["Theta"]   = "Altitude (angle with respect to the horizontal) (in radian)"
COLUMNS_DESC["Phi"]     = "Azimuth (in radian)"
COLUMNS_DESC["X"]       = "X coordinate of shower projection on the ground (in meter)"
COLUMNS_DESC["Y"]       = "Y coordinate of shower projection on the ground (in meter)"
COLUMNS_DESC["Z"]       = "Shower start altitude (in meter)"
COLUMNS_DESC["Ncam"]    = "Number of p.e. in the camera (include NSB and instrument noise)"
COLUMNS_DESC["Type"]    = 'a string with "Reference" or "TC5-10" (for tailcut), "mrfilter ..." (the full command line with option), this allows selecting data sets for the analysis'
COLUMNS_DESC["Success"] = "0 or 1 (allows making statistics, ensure the same number of entries)"
COLUMNS_DESC["hX"]      = "Hillas centroid X"
COLUMNS_DESC["hY"]      = "Hillas centroid Y"
COLUMNS_DESC["hLength"] = "Hillas length"
COLUMNS_DESC["hWidth"]  = "Hillas width"
COLUMNS_DESC["hSize"]   = "Hillas Size (p.e. in the ellipse)"
COLUMNS_DESC["hPsi"]    = "Hillas ellipse angle with respect to the x axis"
COLUMNS_DESC["hSkew"]   = "Hillas skew"
COLUMNS_DESC["hCurt"]   = "Hillas curtosis"
COLUMNS_DESC["hDist"]   = "Distance of centroid to the center (in meters)"
COLUMNS_DESC["hman"]    = "The smallest Manhattan distance of the shower to the border (in pixels)"
COLUMNS_DESC["pe_max1"] = "The highest pe value in the Hillas data (max2, max3 to come later)"
COLUMNS_DESC["pe_min"]  = "The lowest pe value"
COLUMNS_DESC["npix"]    = "Number of (remaining) signal *pixels* in the image (no noise for what concerns the MC)"
COLUMNS_DESC["Dshape"]  = "Epsilon shape"
COLUMNS_DESC["Denergy"] = "Epsilon energy"


#def save_desc(output_file_path, desc_dict):
#    print(output_file_path)
#
#    for key, value in COLUMNS_DESC:
#        print
#


def save(output_file_path, data_array, header_list):
    print(output_file_path)

    if output_file_path.lower().endswith('.csv'):

        # See http://docs.astropy.org/en/stable/io/fits/usage/table.html
        np.savetxt(output_file_path,
                   data_array,
                   fmt="%s",                      # See http://stackoverflow.com/questions/16621351/how-to-use-python-numpy-savetxt-to-write-strings-and-float-number-to-an-ascii-fi
                   delimiter=",",
                   header=",".join(header_list),
                   comments=""                    # String that will be prepended to the ``header`` and ``footer`` strings, to mark them as comments. Default: '# '.
                   )
    else:
        raise Exception('Unknown output format.')


def extract_columns(input_file_path, image_dict, benchmark_dict):

    # Fetch score ###############################

    if "score" in image_dict:
        for score, score_name in zip(image_dict["score"], image_dict["score_name"]):
            if score_name == "e_shape":
                score_e_shape = score
            elif score_name == "e_energy":
                score_e_energy = score

    # Guess the type of particle used ###########

    path_list = image_dict["input_file_path"].lower().strip().split("/")
    if ("gamma" in path_list) and ("proton" not in path_list):
        part = 0
    elif ("proton" in path_list) and ("gamma" not in path_list):
        part = 1
    else:
        part = "unknown"

    # Compute hDist and hman ####################

    cen_x = image_dict["img_cleaned_hillas_2_cen_x"]  if "img_cleaned_hillas_2_cen_x"  in image_dict else None
    cen_y = image_dict["img_cleaned_hillas_2_cen_y"]  if "img_cleaned_hillas_2_cen_y"  in image_dict else None

    if cen_x is not None and cen_y is not None:
        h_dist = math.sqrt(math.pow(cen_x, 2) + math.pow(cen_y, 2))
    else:
        h_dist = "NaN"

    # Make the tuple ############################

    line = collections.OrderedDict()
    line["Part"]    = part
    line["Id"]      = "{}_{}".format(image_dict["event_id"], image_dict["tel_id"])
    line["Evt"]     = image_dict["event_id"]
    line["Tel"]     = image_dict["tel_id"]
    line["Exect"]   = image_dict["execution_time_sec"] if "execution_time_sec" in image_dict else "NaN"
    line["Xtel"]    = image_dict["tel_pos_x"]
    line["Ytel"]    = image_dict["tel_pos_y"]
    line["Ztel"]    = image_dict["tel_pos_z"]
    line["E"]       = image_dict["mc_energy"]
    line["Theta"]   = image_dict["mc_altitude"]
    line["Phi"]     = image_dict["mc_azimuth"]
    line["X"]       = image_dict["mc_core_x"]
    line["Y"]       = image_dict["mc_core_y"]
    line["Z"]       = image_dict["mc_height_first_interaction"]
    #
    line["Ncam"]    = image_dict["img_cleaned_sum_pe"]        # TODO !!!!!           # REF, IN
    line["Type"]    = benchmark_dict["label"]
    #line["Type"]    = benchmark_dict["class_name"]
    line["Success"] = 1 if "score" in image_dict else 0
    line["hX"]      = image_dict["img_cleaned_hillas_2_cen_x"]  if "img_cleaned_hillas_2_cen_x"  in image_dict else "NaN"     # REF
    line["hY"]      = image_dict["img_cleaned_hillas_2_cen_y"]  if "img_cleaned_hillas_2_cen_y"  in image_dict else "NaN"     # REF
    line["hLength"] = image_dict["img_cleaned_hillas_2_length"] if "img_cleaned_hillas_2_length" in image_dict else "NaN"     # REF
    line["hWidth"]  = image_dict["img_cleaned_hillas_2_width"]  if "img_cleaned_hillas_2_width"  in image_dict else "NaN"     # REF
    line["hSize"]   = image_dict["img_cleaned_hillas_2_size"]   if "img_cleaned_hillas_2_size"   in image_dict else "NaN"     # REF
    line["hPsi"]    = image_dict["img_cleaned_hillas_2_psi"]    if "img_cleaned_hillas_2_psi"    in image_dict else "NaN"     # REF
    line["hSkew"]   = "NaN"                       # TODO
    line["hCurt"]   = "NaN"                       # TODO
    line["hDist"]   = h_dist
    line["hman"]    = image_dict["img_ref_signal_to_border_distance"] if "img_ref_signal_to_border_distance" in image_dict else "NaN"
    line["pe_max1"] = image_dict["img_cleaned_max_pe"]        # TODO !!!!!           # REF, IN
    line["pe_min"]  = image_dict["img_cleaned_min_pe"]        # TODO !!!!!           # REF, IN
    line["npix"]    = image_dict["img_cleaned_num_pix"]       # TODO !!!!!           # REF, IN
    line["Dshape"]  = score_e_shape if "score" in image_dict else "NaN"
    line["Denergy"] = score_e_energy if "score" in image_dict else "NaN"

    #(image_dict["input_file_path"]
    #(image_dict["simtel_path"]
    #(image_dict["img_ref_delta_abs_pe"]
    #(image_dict["img_ref_delta_num_pixels"]
    #(image_dict["img_ref_delta_pe"]
    #(image_dict["img_ref_hillas_2_miss"]
    #(image_dict["img_ref_hillas_2_phi"]
    #(image_dict["img_ref_hillas_2_r"]

    return line


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with the tailcut algorithm.")

    parser.add_argument("--output", "-o", required=True, metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The input (JSON) files to convert.")

    args = parser.parse_args()

    output_file_path = args.output
    input_file_list = args.fileargs

    # CONVERT FILES ###########################################################

    global_output_array = None

    for input_file_path in input_file_list:
        print(input_file_path)
        json_dict = common.parse_json_file(input_file_path)

        # Make the file output array
        io_list = json_dict["io"]
        file_output_list = [list(extract_columns(input_file_path, image_dict, json_dict).values()) for image_dict in io_list]
        file_output_array = np.array(file_output_list)

        # Append the file output array to the global ouput array
        if global_output_array is None:
            global_output_array = file_output_array
        else:
            global_output_array = np.vstack([global_output_array, file_output_array])

    # SAVE FILE ###############################################################

    save(output_file_path,
         global_output_array,
         list(COLUMNS_DESC.keys()))


if __name__ == "__main__":
    main()

