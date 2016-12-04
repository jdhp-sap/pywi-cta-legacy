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

"""
Convert benchmark's JSON files to flat files.
"""

import common_functions as common

import argparse
import numpy as np
import os


def save_csv(output_file_path, data_array, header_list):
    print(output_file_path)

    # See http://docs.astropy.org/en/stable/io/fits/usage/table.html
    np.savetxt(output_file_path,
               data_array,
               fmt="%s",                      # See http://stackoverflow.com/questions/16621351/how-to-use-python-numpy-savetxt-to-write-strings-and-float-number-to-an-ascii-fi
               delimiter=",",
               header=",".join(header_list),
               comments=""                 # String that will be prepended to the ``header`` and ``footer`` strings, to mark them as comments. Default: '# '.
               )

def extract_columns(image_dict):
    line = [
            image_dict["event_id"],
            image_dict["tel_id"],
            image_dict["npe"],
            image_dict["input_file_path"],
            image_dict["execution_time"],
            image_dict["ev_count"],
            image_dict["mc_energy"],
            image_dict["mc_energy_unit"],
            image_dict["mc_altitude"],
            image_dict["mc_altitude_unit"],
            image_dict["mc_azimuth"],
            image_dict["mc_azimuth_unit"],
            image_dict["mc_core_x"],
            image_dict["mc_core_x_unit"],
            image_dict["mc_core_y"],
            image_dict["mc_core_y_unit"],
            image_dict["mc_height_first_interaction"],
            image_dict["mc_height_first_interaction_unit"],
            image_dict["num_tel_with_data"],
            image_dict["num_tel_with_trigger"],
            image_dict["optical_foclen"],
            image_dict["optical_foclen_unit"],
            image_dict["run_id"],
            image_dict["simtel_path"],
            image_dict["tel_pos_x"],
            image_dict["tel_pos_x_unit"],
            image_dict["tel_pos_y"],
            image_dict["tel_pos_y_unit"],
            image_dict["tel_pos_z"],
            image_dict["tel_pos_z_unit"]
           ]

    for index, (score, score_name) in enumerate(zip(image_dict["score"], image_dict["score_name"])):
        #print(index, score_name, score)

        if score_name in score_name_list:
            if score_name_list.index(score_name) == index:
                line.append(score)
            else:
                raise(Exception("Inconsistent data: wrong index"))
        else:
            score_name_list.append(score_name)
            line.append(score)

    return line


OUTPUT_HEADER_LIST = [
                      "JSON input file",
                      "Event ID",
                      "Tel ID",
                      "NPE",
                      "FITS input file",
                      "Execution time",
                      "EV count",
                      "MC energy",
                      "mC energy unit",
                      "MC altitude",
                      "MC altitude unit",
                      "MC azimuth",
                      "MC azimuth unit",
                      "MC core x",
                      "MC core x unit",
                      "MC core y",
                      "MC core y unit",
                      "MC height first interaction",
                      "MC height first interaction unit",
                      "Num tel with data",
                      "Num tel with trigger",
                      "Optical foclen",
                      "Optical foclen unit",
                      "Run id",
                      "Simtel path",
                      "Tel pos x",
                      "Tel pos x unit",
                      "Tel pos y",
                      "Tel pos y unit",
                      "Tel pos z",
                      "Tel pos z unit"
                     ]
#OUTPUT_DTYPE_LIST = ['', '', '', '', '', '', '']

score_name_list = []


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

        common_lines = [input_file_path]

        # Make the file output array
        io_list = json_dict["io"]
        file_output_list = [common_lines + extract_columns(image_dict) for image_dict in io_list if "score" in image_dict]
        file_output_array = np.array(file_output_list)

        # Append the file output array to the global ouput array
        if global_output_array is None:
            global_output_array = file_output_array
        else:
            global_output_array = np.vstack([global_output_array, file_output_array])

    # SAVE FILE ###############################################################

    save_csv(output_file_path, global_output_array, OUTPUT_HEADER_LIST + score_name_list)


if __name__ == "__main__":
    main()

