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

__all__ = ['ObjectiveFunction']

import numpy as np

from datapipe.denoising.wavelets_mrfilter import WaveletTransform
from datapipe.benchmark import assess

# OPTIMIZER ##################################################################

class ObjectiveFunction:

    def __init__(self, input_files):
        self.call_number = 0

        # Init the wavelet class
        self.cleaning_algorithm = WaveletTransform()

        # Make the image list
        self.input_files = input_files

        # PRE PROCESSING FILTERING ############################################

        # TODO...


    def __call__(self, algo_params_var):
        self.call_number += 1

        benchmark_method = "all"          # TODO

        label = "WT_{}".format(self.call_number)
        self.cleaning_algorithm.label = label

        output_file_path = "score_wavelets_optim_{}.json".format(self.call_number)

        algo_params = {
                    "coef_detection_method": 1,
                    "correction_offset": False,
                    "detect_only_positive_structure": False,
                    "epsilon": None,
                    "first_detection_scale": None,
                    "input_image_scale": "linear",
                    #"k_sigma_noise_threshold": "2,2,3,3",
                    "kill_isolated_pixels": True,
                    "mask_file_path": None,
                    #"mrfilter_directory": "/Volumes/ramdisk",
                    "nan_noise_lambda": 0,
                    "nan_noise_mu": 0,
                    "nan_noise_sigma": 0,
                    "noise_model": 3,
                    "number_of_iterations": None,
                    "number_of_scales": 4,
                    "offset_after_calibration": None,
                    "precision": None,
                    "support_file_name": None,
                    "suppress_isolated_pixels": True,
                    "suppress_last_scale": True,
                    "suppress_positivity_constraint": False,
                    "tmp_files_directory": "/Volumes/ramdisk",
                    "type_of_filtering": None,
                    "type_of_filters": None,
                    "type_of_multiresolution_transform": None,
                    "type_of_non_orthog_filters": None,
                    "verbose": False
                }

        algo_params.update(algo_params_var)

        # TODO: randomly make a subset fo self.input_files
        input_files = self.input_files

        output_dict = self.cleaning_algorithm.run(algo_params,
                                                  input_file_or_dir_path_list=input_files,
                                                  benchmark_method=benchmark_method,
                                                  output_file_path=output_file_path)

        #print(output_dict)

        score_list = []

        # Read and compute results from output_dict
        for image_dict in output_dict["io"]:

            # POST PROCESSING FILTERING #######################################

            # >>>TODO<<<: Filter images: decide wether the image should be used or not ? (contained vs not contained)
            # TODO: filter these images *before* cleaning them to avoid waste of computation...

            # >>>TODO<<<: Filter images by energy range: decide wether the image should be used or not ?
            # TODO: filter these images *before* cleaning them to avoid waste of computation...

            ###################################################################

            # !!!>>>TODO<<<!!!: Asses the cleaned image
#            wt_hillas_score  = assess.metric_hillas_delta2(input_img, output_image, reference_image, pixels_position, params=None)
#            ref_hillas_score = assess.metric_hillas_delta2(ref_img,   output_image, reference_image, pixels_position, params=None)
#
#            wt_psi  = hillas_params_2_cleaned_img.psi.to(u.rad).value
#            ref_psi = hillas_params_2_cleaned_img.psi.to(u.rad).value
#
#            # Compute and normalize the delta psi
#            delta_psi = np.fmod(((ref_psi - wt_psi) * 180. / np.pi), 90.)
#            delta_psi = abs(delta_psi)

            #score_index = image_dict["score_name"].find("hillas2_delta_psi")
            if "img_cleaned_hillas_2_psi" in image_dict:
                delta_psi = image_dict["img_cleaned_hillas_2_psi"]  # image_dict["score"][score_index]   # TODO: WHY ARE THERE MULTIPLE RESULTS "DELTAPSI": image_dict["img_cleaned_hillas_2_psi"], image_dict["score"][...], ... ???
                score_list.append(delta_psi)

        # Compute the mean
        score = np.array([score_list]).mean()

        # TODO: save results in a JSON file (?)

        return score


if __name__ == "__main__":
    # Test...

    #func = ObjectiveFunction(input_files=["/Users/jdecock/astri_data/fits/gamma/"])
    func = ObjectiveFunction(input_files=["./testset/gamma/astri/tel1/"])

    algo_params_var = {
                "k_sigma_noise_threshold": "2"
            }

    score = func(algo_params_var)

    #algo_params_var = {
    #            "k_sigma_noise_threshold": "3"
    #        }

    #score = func(algo_params_var)

    print(score)

