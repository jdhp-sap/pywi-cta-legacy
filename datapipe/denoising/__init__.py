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

import datetime
import json
import os
import numpy as np
import sys
import time
import traceback

from datapipe.benchmark import assess
from datapipe.io import images

__all__ = ['fft',
           'null',
           'tailcut',
           'tailcut_jd',
           'wavelets_mrfilter',
           'wavelets_mrtransform']

# TODO: params algos

def run(cleaning_function,
        cleaning_function_params,
        input_file_or_dir_path_list,
        benchmark_method,
        output_file_path,
        cleaning_algorithm_label,
        plot=False,
        saveplot=None):

    if benchmark_method is not None:
        io_list = []

    for input_file_or_dir_path in input_file_or_dir_path_list:

        if os.path.isdir(input_file_or_dir_path):
            input_file_path_list = []
            for dir_item in os.listdir(input_file_or_dir_path):
                dir_item_path = os.path.join(input_file_or_dir_path, dir_item)
                if dir_item_path.lower().endswith('.fits') and os.path.isfile(dir_item_path):
                    input_file_path_list.append(dir_item_path)
        else:
            input_file_path_list = [input_file_or_dir_path]

        for input_file_path in input_file_path_list:

            # CLEAN ONE IMAGE #########################################################

            image_dict = {"input_file_path": input_file_path}

            try:
                # READ THE INPUT FILE #################################################

                input_img, reference_img, metadata_dict = images.load_benchmark_images(input_file_path)

                image_dict.update(metadata_dict)

                # CLEAN THE INPUT IMAGE ###############################################

                initial_time = time.perf_counter()
                cleaned_img = cleaning_function(input_img, **cleaning_function_params)
                execution_time = time.perf_counter() - initial_time

                # ASSESS OR PRINT THE CLEANED IMAGE ###################################

                if benchmark_method is not None:
                    score_tuple = assess.assess_image_cleaning(input_img,
                                                               cleaned_img,
                                                               reference_img,
                                                               benchmark_method)

                    image_dict["score"] = score_tuple
                    image_dict["execution_time"] = execution_time

                # PLOT IMAGES #########################################################

                if plot or (saveplot is not None):
                    image_list = [input_img, reference_img, cleaned_img] 
                    title_list = ["Input image", "Reference image", "Cleaned image"] 

                    if plot:
                        images.plot_list(image_list, title_list)

                    if saveplot is not None:
                        images.mpl_save_list(image_list, saveplot, title_list)

            except Exception as e:
                print("Abort image {}: {} ({})".format(input_file_path, e, type(e)))
                #traceback.print_tb(e.__traceback__, file=sys.stdout)

                if benchmark_method is not None:
                    error_dict = {"type": str(type(e)),
                                  "message": str(e)}
                    image_dict["error"] = error_dict

            finally:
                if benchmark_method is not None:
                    io_list.append(image_dict)

    if benchmark_method is not None:
        error_list = [image_dict["error"] for image_dict in io_list if "error" in image_dict]
        print("{} images aborted".format(len(error_list)))

        output_dict = {}
        output_dict["algo_name"] = cleaning_function.__name__
        output_dict["algo_code_ref"] = str(cleaning_function.__code__)
        output_dict["label"] = cleaning_algorithm_label
        output_dict["algo_params"] = cleaning_function_params
        output_dict["benchmark_method"] = benchmark_method
        output_dict["date_time"] = str(datetime.datetime.now())
        output_dict["system"] = " ".join(os.uname())
        output_dict["io"] = io_list

        with open(output_file_path, "w") as fd:
            json.dump(output_dict, fd, sort_keys=True, indent=4)  # pretty print format
