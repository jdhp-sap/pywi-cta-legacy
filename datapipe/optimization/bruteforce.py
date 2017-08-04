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

__all__ = ['Minimize']

from datapipe.optimization.objectivefunc.wavelets_mrfilter import ObjectiveFunction

# EXCEPTIONS #################################################################

class OptimizationError(Exception):
    pass


# OPTIMIZER ##################################################################

class Minimize:

    def __init__(self):
        pass

    def __call__(self, objective_function, input_file_or_dir_path_list ):
    """Optimize with the brute-force method."""

        # Set params (TODO)
        type_of_multiresolution_transform = None
        type_of_filters = None
        type_of_non_orthog_filters = None
        number_of_scales = 4
        suppress_last_scale = False
        suppress_isolated_pixels = False
        kill_isolated_pixels = False
        coef_detection_method = None
        k_sigma_noise_threshold = None
        noise_model = None
        detect_only_positive_structure = False
        suppress_positivity_constraint = False
        type_of_filtering = None
        first_detection_scale = None
        number_of_iterations = None
        epsilon = None
        support_file_name = None
        precision = None
        mask_file_path = None
        offset_after_calibration = None
        correction_offset = None
        input_image_scale = None
        verbose = False
        tmp_dir = "."
    
        cleaning_function_params = {
                    "type_of_multiresolution_transform": type_of_multiresolution_transform,
                    "type_of_filters": type_of_filters,
                    "type_of_non_orthog_filters": type_of_non_orthog_filters,
                    "number_of_scales": number_of_scales,
                    "suppress_last_scale": suppress_last_scale,
                    "suppress_isolated_pixels": suppress_isolated_pixels,
                    "kill_isolated_pixels": kill_isolated_pixels,
                    "coef_detection_method": coef_detection_method,
                    "k_sigma_noise_threshold": k_sigma_noise_threshold,
                    "noise_model": noise_model,
                    "detect_only_positive_structure": detect_only_positive_structure,
                    "suppress_positivity_constraint": suppress_positivity_constraint,
                    "type_of_filtering": type_of_filtering,
                    "first_detection_scale": first_detection_scale,
                    "number_of_iterations": number_of_iterations,
                    "epsilon": epsilon,
                    "support_file_name": support_file_name,
                    "precision": precision,
                    "mask_file_path": mask_file_path,
                    "offset_after_calibration": offset_after_calibration,
                    "correction_offset": correction_offset,
                    "input_image_scale": input_image_scale,
                    "verbose": verbose,
                    "tmp_files_directory": tmp_dir,
                    #"mrfilter_directory": "/Volumes/ramdisk"
                }

        # Evaluate params
        error = objective_function(cleaning_function_params, input_file_or_dir_path_list)

        # Return best params (TODO)

def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")


    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    input_file_or_dir_path_list = args.fileargs

    optimizer = Minimize()
    objective_function = ObjectiveFunction()

    optimizer.minimize(objective_function, input_file_or_dir_path_list)


if __name__ == "__main__":
    main()

