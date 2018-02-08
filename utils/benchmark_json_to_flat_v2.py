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

import argparse
import collections
import numpy as np
import math
import json
import os


COLUMNS_DESC = collections.OrderedDict()
COLUMNS_DESC["Part"]     = "Particle, 0:gamma, -1:electron/positron, 1:proton (iron would be 26)"
COLUMNS_DESC["Id"]       = "A string built like this : event#_telescope#, see below (e.g telescope 1 and event 84 gives 84_1)"
COLUMNS_DESC["Evt"]      = "Event ID"
COLUMNS_DESC["Tel"]      = "Telescope ID"
COLUMNS_DESC["Exect"]    = "Execution time (in second)"
COLUMNS_DESC["Xtel"]     = "x coordinates of telescope (in meter)"
COLUMNS_DESC["Ytel"]     = "y coordinates of telescope (in meter)"
COLUMNS_DESC["Ztel"]     = "z coordinates of telescope (in meter)"
COLUMNS_DESC["E"]        = "Event energy (in TeV)"
COLUMNS_DESC["Theta"]    = "Altitude (angle with respect to the horizontal) (in radian)"
COLUMNS_DESC["Phi"]      = "Azimuth (in radian)"
COLUMNS_DESC["X"]        = "X coordinate of shower projection on the ground (in meter)"
COLUMNS_DESC["Y"]        = "Y coordinate of shower projection on the ground (in meter)"
COLUMNS_DESC["Z"]        = "Shower start altitude (in meter)"
COLUMNS_DESC["peSum"]    = "Number of p.e. in the camera (include NSB and instrument noise)"
COLUMNS_DESC["Type"]     = 'a string with "Reference" or "TC5-10" (for tailcut), "mrfilter ..." (the full command line with option), this allows selecting data sets for the analysis'
COLUMNS_DESC["Success"]  = "0 or 1 (allows making statistics, ensure the same number of entries)"
COLUMNS_DESC["hX"]       = "Hillas centroid X"
COLUMNS_DESC["hY"]       = "Hillas centroid Y"
COLUMNS_DESC["hLength"]  = "Hillas length"
COLUMNS_DESC["hWidth"]   = "Hillas width"
COLUMNS_DESC["hSize"]    = "Hillas Size (p.e. in the ellipse)"
COLUMNS_DESC["hPsi"]     = "Hillas ellipse angle with respect to the x axis"
COLUMNS_DESC["hPhi"]     = "Hillas Phi"
COLUMNS_DESC["hMiss"]    = "Hillas Miss (distance of the major axis to the center of view in meter)"
COLUMNS_DESC["hR"]       = "Hillas R"
COLUMNS_DESC["hSkew"]    = "Hillas skew"
COLUMNS_DESC["hKurt"]    = "Hillas kurtosis"
COLUMNS_DESC["hDist"]    = "Distance of centroid to the center (in meters)"
COLUMNS_DESC["nIsl"]     = "Number or cleaned islands"
COLUMNS_DESC["DNpeIsl"]  = "PE sum in cleaned islands"
COLUMNS_DESC["DNpixIsl"] = "Number of pixels in cleaned islands"
COLUMNS_DESC["peMaxB"]   = "PE max of pixels on the border of the image"
COLUMNS_DESC["border"]   = "The smallest Manhattan distance of the shower to the border (in pixels)"
COLUMNS_DESC["peMax1"]   = "The highest pe value in the Hillas data (max2, max3 to come later)"
COLUMNS_DESC["peMin"]    = "The lowest pe value"
COLUMNS_DESC["nPix"]     = "Number of (remaining) signal *pixels* in the image (no noise for what concerns the MC)"
COLUMNS_DESC["Dshape"]   = "Epsilon shape"
COLUMNS_DESC["Denergy"]  = "Epsilon energy"
COLUMNS_DESC["fits"]     = "Name of the Fits file the data came from"
COLUMNS_DESC["cam"]      = "Name of the camera (ASTRI, GCT, ...)"


#def save_desc(output_file_path, desc_dict):
#    print(output_file_path)
#
#    for key, value in COLUMNS_DESC:
#        print
#


def parse_json_file(json_file_path):
    with open(json_file_path, "r") as fd:
        json_data = json.load(fd)
    return json_data


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

    print("{}_{}".format(image_dict["event_id"], image_dict["tel_id"]))

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


    # Retro-compatibility workaround ##############

    if "cam_id" not in image_dict:
        image_dict["cam_id"] = "ASTRI_CROPPED"

    # Compute hDist ###############################

    cen_x = image_dict["img_cleaned_hillas_2_cen_x"]  if "img_cleaned_hillas_2_cen_x"  in image_dict else None
    cen_y = image_dict["img_cleaned_hillas_2_cen_y"]  if "img_cleaned_hillas_2_cen_y"  in image_dict else None

    if cen_x is not None and cen_y is not None:
        #h_dist = math.sqrt(math.pow(cen_x, 2) + math.pow(cen_y, 2))   # distance to the center

        if image_dict["cam_id"] in ("ASTRI", "ASTRI_CROPPED"):
            camera_size = 0.14255599677562714      # TODO: this is a hardcoded value for cropped ASTRI cameras
            h_dist = min(camera_size - abs(cen_x), camera_size - abs(cen_y))
        else:
            h_dist = "NaN"
    else:
        h_dist = "NaN"

    # Make the tuple ############################

    line = collections.OrderedDict()
    line["Part"]    = part
    line["Id"]      = "{}_{}".format(image_dict["event_id"], image_dict["tel_id"])
    line["Evt"]     = image_dict["event_id"]
    line["Tel"]     = image_dict["tel_id"]
    line["Exect"]   = image_dict["full_clean_execution_time_sec"] if "full_clean_execution_time_sec" in image_dict else "NaN"
    line["Xtel"]    = image_dict["tel_pos_x"] if "tel_pos_x_unit" in image_dict else image_dict["tel_pos_x"][0]
    line["Ytel"]    = image_dict["tel_pos_y"] if "tel_pos_y_unit" in image_dict else image_dict["tel_pos_y"][0]
    line["Ztel"]    = image_dict["tel_pos_z"] if "tel_pos_z_unit" in image_dict else image_dict["tel_pos_z"][0]
    line["E"]       = image_dict["mc_energy"] if "mc_energy_unit" in image_dict else image_dict["mc_energy"][0]
    line["Theta"]   = image_dict["mc_altitude"] if "mc_altitude_unit" in image_dict else image_dict["mc_altitude"][0]
    line["Phi"]     = image_dict["mc_azimuth"] if "mc_azimuth_unit" in image_dict else image_dict["mc_azimuth"][0]
    line["X"]       = image_dict["mc_core_x"] if "mc_core_x_unit" in image_dict else image_dict["mc_core_x"][0]
    line["Y"]       = image_dict["mc_core_y"] if "mc_core_y_unit" in image_dict else image_dict["mc_core_y"][0]
    line["Z"]       = image_dict["mc_height_first_interaction"] if "mc_height_first_interaction_unit" in image_dict else image_dict["mc_height_first_interaction"][0]
    #
    line["peSum"]   = image_dict["img_cleaned_sum_pe"] if "img_cleaned_sum_pe"  in image_dict else "NaN"        # TODO !!!!!           # REF, IN
    line["Type"]    = benchmark_dict["label"]
    #line["Type"]    = benchmark_dict["class_name"]
    line["Success"] = 1 if "score" in image_dict else 0
    #
    line["hX"]      = image_dict["img_cleaned_hillas_2_cen_x"]    if "img_cleaned_hillas_2_cen_x"    in image_dict else "NaN"
    line["hY"]      = image_dict["img_cleaned_hillas_2_cen_y"]    if "img_cleaned_hillas_2_cen_y"    in image_dict else "NaN"
    line["hLength"] = image_dict["img_cleaned_hillas_2_length"]   if "img_cleaned_hillas_2_length"   in image_dict else "NaN"
    line["hWidth"]  = image_dict["img_cleaned_hillas_2_width"]    if "img_cleaned_hillas_2_width"    in image_dict else "NaN"
    line["hSize"]   = image_dict["img_cleaned_hillas_2_size"]     if "img_cleaned_hillas_2_size"     in image_dict else "NaN"
    line["hPsi"]    = image_dict["img_cleaned_hillas_2_psi"]      if "img_cleaned_hillas_2_psi"      in image_dict else "NaN"
    line["hPhi"]    = image_dict["img_cleaned_hillas_2_phi"]      if "img_cleaned_hillas_2_phi"      in image_dict else "NaN"
    line["hMiss"]   = image_dict["img_cleaned_hillas_2_miss"]     if "img_cleaned_hillas_2_miss"     in image_dict else "NaN"
    line["hR"]      = image_dict["img_cleaned_hillas_2_r"]        if "img_cleaned_hillas_2_r"        in image_dict else "NaN"
    line["hSkew"]   = image_dict["img_cleaned_hillas_2_skewness"] if "img_cleaned_hillas_2_skewness" in image_dict else "NaN"
    line["hKurt"]   = image_dict["img_cleaned_hillas_2_kurtosis"] if "img_cleaned_hillas_2_kurtosis" in image_dict else "NaN"
    line["hDist"]   = h_dist
    #
    line["nIsl"]     = image_dict["img_cleaned_num_islands"]              if "img_cleaned_num_islands"              in image_dict else "NaN"
    line["DNpeIsl"]  = image_dict["img_cleaned_islands_delta_abs_pe"]     if "img_cleaned_islands_delta_abs_pe"     in image_dict else "NaN"
    line["DNpixIsl"] = image_dict["img_cleaned_islands_delta_num_pixels"] if "img_cleaned_islands_delta_num_pixels" in image_dict else "NaN"
    #
    line["peMaxB"]  = image_dict["img_cleaned_pemax_on_border"]           if "img_cleaned_pemax_on_border"           in image_dict else "NaN"
    line["border"]  = image_dict["img_cleaned_signal_to_border_distance"] if "img_cleaned_signal_to_border_distance" in image_dict else "NaN"
    line["peMax1"]  = image_dict["img_cleaned_max_pe"]  if "img_cleaned_max_pe"  in image_dict else "NaN"     # TODO !!!!!
    line["peMin"]   = image_dict["img_cleaned_min_pe"]  if "img_cleaned_min_pe"  in image_dict else "NaN"     # TODO !!!!!
    line["nPix"]    = image_dict["img_cleaned_num_pix"] if "img_cleaned_num_pix" in image_dict else "NaN"     # TODO !!!!!
    line["Dshape"]  = score_e_shape  if "score" in image_dict else "NaN"
    line["Denergy"] = score_e_energy if "score" in image_dict else "NaN"
    line["fits"]    = os.path.basename(image_dict["input_file_path"]) if "input_file_path" in image_dict else "NaN"
    line["cam"]     = image_dict["cam_id"] if "cam_id" in image_dict else "NaN"

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
        json_dict = parse_json_file(input_file_path)

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

