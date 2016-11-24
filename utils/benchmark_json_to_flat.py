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


def save_np_array(output_file_path, data_array, header_list):
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
    line = [image_dict["event_id"],
            image_dict["tel_id"],
            image_dict["mc_energy"],
            image_dict["npe"],
            image_dict["score"][0],
            image_dict["score"][1]
           ]
    return line


OUTPUT_HEADER_LIST = ["JSON input file", "Event ID", "Tel ID", "MC energy", "NPE", "E shape", "E energy"]
#OUTPUT_DTYPE_LIST = ['', '', '', '', '', '', '']


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

    save_np_array(output_file_path, global_output_array, OUTPUT_HEADER_LIST)


if __name__ == "__main__":
    main()

