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

Each line is one image.

- "JSON input file".................. : the JSON output file the data come from (indicate the configuration used, e.g. wavelets, tailcut, ...)
- "Event ID"
- "Tel ID"
- "NPE".............................. : the total number of photoelectrons in the image
- "FITS input file".................. : the name of the input file (which contain the noisy and the pure signal version of the image)
- "Execution time"
- "EV count"......................... : same as simtel
- "MC energy"........................ : montecarlo energy in TeV
- "mC energy unit"
- "MC altitude"
- "MC altitude unit"
- "MC azimuth"....................... : same as simtel
- "MC azimuth unit"
- "MC core x"........................ : same as simtel
- "MC core x unit"
- "MC core y"........................ : same as simtel
- "MC core y unit"
- "MC height first interaction"...... : same as simtel
- "MC height first interaction unit"
- "Num tel with data"................ : same as simtel
- "Num tel with trigger"............. : same as simtel
- "Optical foclen"................... : same as simtel
- "Optical foclen unit"
- "Run id"........................... : same as simtel
- "Simtel path"...................... : the simtel file used to make the "FITS input file"
- "Tel pos x"........................ : same as simtel
- "Tel pos x unit"
- "Tel pos y"........................ : same as simtel
- "Tel pos y unit"
- "Tel pos z"........................ : same as simtel
- "Tel pos z unit"
- "Img ref delta abs pe"............. : number of PE removed by the island cleaning on the reference image (sum(abs(original_img - filtered_img)))
- "Img ref delta num pixels"......... : number of pixels (not their value) removed by the island cleaning on the reference image
- "Img ref delta pe"................. : number of PE removed by the island cleaning on the reference image (sum(original_img - filtered_img))
- "Img ref hillas 2 cen x"........... : hillas parameter "cen x" on the reference (pure signal) image
- "Img ref hillas 2 cen y"........... : hillas parameter "cen y" on the reference (pure signal) image
- "Img ref hillas 2 length".......... : hillas parameter "length" on the reference (pure signal) image
- "Img ref hillas 2 miss"............ : hillas parameter "miss" on the reference (pure signal) image
- "Img ref hillas 2 phi"............. : hillas parameter "phi" on the reference (pure signal) image
- "Img ref hillas 2 psi"............. : hillas parameter "psi" on the reference (pure signal) image
- "Img ref hillas 2 psi norm"........ : normalized hillas parameter "psi" on the reference (pure signal) image (abs(sin(radian(psi))))
- "Img ref hillas 2 r"............... : hillas parameter "r" on the reference (pure signal) image
- "Img ref hillas 2 size"............ : hillas parameter "size" on the reference (pure signal) image
- "Img ref hillas 2 width"........... : hillas parameter "width" on the reference (pure signal) image
- "Img ref signal to border distance" : the smallest Manhattan distance of the pure signal to any border of the image
- "Min npe".......................... : the lowest pixel value in the image
- "Max npe".......................... : the highest pixel value in the image

For "metrics" headers, see http://www.jdhp.org/software/sap-cta-data-pipeline/api_benchmark_assess.html
"""

import common_functions as common

import argparse
import astropy.table
import numpy as np
import os


def save(output_file_path, data_array, header_list, dtype_list):
    print(output_file_path)

    if output_file_path.lower().endswith('.csv'):

        # See http://docs.astropy.org/en/stable/io/fits/usage/table.html
        np.savetxt(output_file_path,
                   data_array,
                   fmt="%s",                      # See http://stackoverflow.com/questions/16621351/how-to-use-python-numpy-savetxt-to-write-strings-and-float-number-to-an-ascii-fi
                   delimiter=",",
                   header=",".join(header_list),
                   comments=""                 # String that will be prepended to the ``header`` and ``footer`` strings, to mark them as comments. Default: '# '.
                   )

    elif output_file_path.lower().endswith(('.fits', '.fit')):

        table = astropy.table.Table(names=header_list, dtype=dtype_list)

        for row in data_array:
            table.add_row(row)

        #print(table)
        table.write(output_file_path, overwrite=True)

    else:
        raise Exception('Unknown output format.')


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
            image_dict["tel_pos_z_unit"],
            image_dict["img_ref_delta_abs_pe"],
            image_dict["img_ref_delta_num_pixels"],
            image_dict["img_ref_delta_pe"],
            image_dict["img_ref_hillas_2_cen_x"],
            image_dict["img_ref_hillas_2_cen_y"],
            image_dict["img_ref_hillas_2_length"],
            image_dict["img_ref_hillas_2_miss"],
            image_dict["img_ref_hillas_2_phi"],
            image_dict["img_ref_hillas_2_psi"],
            image_dict["img_ref_hillas_2_psi_norm"],
            image_dict["img_ref_hillas_2_r"],
            image_dict["img_ref_hillas_2_size"],
            image_dict["img_ref_hillas_2_width"],
            image_dict["img_ref_signal_to_border_distance"],
            image_dict["min_npe"],
            image_dict["max_npe"]
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
                      "Tel pos z unit",
                      "Img ref delta abs pe",
                      "Img ref delta num pixels",
                      "Img ref delta pe",
                      "Img ref hillas 2 cen x",
                      "Img ref hillas 2 cen y",
                      "Img ref hillas 2 length",
                      "Img ref hillas 2 miss",
                      "Img ref hillas 2 phi",
                      "Img ref hillas 2 psi",
                      "Img ref hillas 2 psi norm",
                      "Img ref hillas 2 r",
                      "Img ref hillas 2 size",
                      "Img ref hillas 2 width",
                      "Img ref signal to border distance",
                      "Min npe",
                      "Max npe"
                     ]

OUTPUT_DTYPE_LIST = [
                     "S256", # JSON input file
                     "i4",   # Event ID
                     "i4",   # Tel ID
                     "f8",   # NPE
                     "S256", # FITS input file
                     "f8",   # Execution time
                     "i4",   # EV count
                     "f8",   # MC energy
                     "S16",  # mC energy unit
                     "f8",   # MC altitude
                     "S16",  # MC altitude unit
                     "f8",   # MC azimuth
                     "S16",  # MC azimuth unit
                     "f8",   # MC core x
                     "S16",  # MC core x unit
                     "f8",   # MC core y
                     "S16",  # MC core y unit
                     "f8",   # MC height first interaction
                     "S16",  # MC height first interaction unit
                     "i4",   # Num tel with data
                     "i4",   # Num tel with trigger
                     "f8",   # Optical foclen
                     "S16",  # Optical foclen unit
                     "i4",   # Run id
                     "S256", # Simtel path
                     "f8",   # Tel pos x
                     "S16",  # Tel pos x unit
                     "f8",   # Tel pos y
                     "S16",  # Tel pos y unit
                     "f8",   # Tel pos z
                     "S16",  # Tel pos z unit
                     "f8",   # Img ref delta abs pe
                     "f8",   # Img ref delta num pixels
                     "f8",   # Img ref delta pe
                     "f8",   # Img ref hillas 2 cen x
                     "f8",   # Img ref hillas 2 cen y
                     "f8",   # Img ref hillas 2 length
                     "f8",   # Img ref hillas 2 miss
                     "f8",   # Img ref hillas 2 phi
                     "f8",   # Img ref hillas 2 psi
                     "f8",   # Img ref hillas 2 psi norm
                     "f8",   # Img ref hillas 2 r
                     "f8",   # Img ref hillas 2 size
                     "f8",   # Img ref hillas 2 width
                     "f8",   # Img ref signal to border distance
                     "f8",   # Min npe
                     "f8",   # Max npe
                    ]

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

    save(output_file_path,
         global_output_array,
         OUTPUT_HEADER_LIST + score_name_list,
         OUTPUT_DTYPE_LIST + ["f8",] * len(score_name_list))


if __name__ == "__main__":
    main()

