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

from datapipe.denoising.tailcut import Tailcut
from datapipe.benchmark import assess


def norm_angle_diff(angle_in_degrees):
    """Normalize the difference of 2 angles in degree.

    This function is used to normalize the "delta psi" angle.
    """
    return np.abs(np.mod(angle_in_degrees + 90, 180) - 90.)


# OPTIMIZER ##################################################################

class ObjectiveFunction:

    def __init__(self, input_files, geom=None, max_num_img=None, aggregation_method="mean"):
        self.call_number = 0

        # Init the wavelet class
        self.cleaning_algorithm = Tailcut()

        # Make the image list
        self.input_files = input_files
        self.max_num_img = max_num_img

        self.geom = geom

        self.aggregation_method = aggregation_method  # "mean" or "median"

        print("aggregation method:", self.aggregation_method)

        # PRE PROCESSING FILTERING ############################################

        # TODO...


    def __call__(self, threshold_list):
        self.call_number += 1

        aggregated_score = np.inf

        try:
            high_threshold = threshold_list[0]
            low_threshold = threshold_list[1]
            low_threshold = min(low_threshold, high_threshold)  # low threshold should not be greater than high threshold

            algo_params_var = {
                        "high_threshold": high_threshold,
                        "low_threshold": low_threshold
                    }

            benchmark_method = "delta_psi"          # TODO

            label = "TC_{}".format(self.call_number)
            self.cleaning_algorithm.label = label

            output_file_path = "score_tailcut_optim_{}.json".format(self.call_number)

            algo_params = {
                        "kill_isolated_pixels": True,
                        "verbose": False,
                        "geom": self.geom
                    }

            algo_params.update(algo_params_var)

            # TODO: randomly make a subset fo self.input_files
            input_files = self.input_files

            output_dict = self.cleaning_algorithm.run(algo_params,
                                                      input_file_or_dir_path_list=input_files,
                                                      benchmark_method=benchmark_method,
                                                      output_file_path=output_file_path,
                                                      max_num_img=self.max_num_img)

            score_list = []

            # Read and compute results from output_dict
            for image_dict in output_dict["io"]:

                # POST PROCESSING FILTERING #######################################

                # >>>TODO<<<: Filter images: decide wether the image should be used or not ? (contained vs not contained)
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                # >>>TODO<<<: Filter images by energy range: decide wether the image should be used or not ?
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                ###################################################################

                # GET THE CLEANED IMAGE SCORE

                if ("img_ref_hillas_2_psi" not in image_dict) or ("img_cleaned_hillas_2_psi" not in image_dict):
                    raise Exception("Cannot get the score")

                output_image_parameter_psi_rad = image_dict["img_ref_hillas_2_psi"]
                reference_image_parameter_psi_rad = image_dict["img_cleaned_hillas_2_psi"]
                delta_psi_rad = reference_image_parameter_psi_rad - output_image_parameter_psi_rad
                normalized_delta_psi_deg = norm_angle_diff(np.degrees(delta_psi_rad))

                if image_dict["score_name"][0] != "delta_psi":
                    raise Exception("Cannot get the score")

                normalized_delta_psi_deg = image_dict["score"][0]

                score_list.append(normalized_delta_psi_deg)

            # Compute the mean
            if self.aggregation_method == "mean":
                aggregated_score = np.array([score_list]).mean()
            elif self.aggregation_method == "median":
                aggregated_score = np.array([score_list]).median()
            else:
                raise ValueError("Unknown value for aggregation_method: {}".format(self.aggregation_method))

            # TODO: save results in a JSON file (?)
            print(algo_params_var, aggregated_score, self.aggregation_method)
        except Exception as e:
            print(e)

        return aggregated_score


if __name__ == "__main__":
    # Test...

    #func = ObjectiveFunction(input_files=["./MISC/testset/gamma/digicam/"])
    func = ObjectiveFunction(input_files=["/dev/shm/.jd/digicam/gamma/"])

    threshold_list = [10, 5]

    score = func(threshold_list)

