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

from datapipe.denoising import WaveletTransform

# OPTIMIZER ##################################################################

class ObjectiveFunction:

    def __init__(self):
        self.call_number = 0

    def __call__(self, cleaning_function_params, input_file_or_dir_path_list):
        self.call_number += 1

        benchmark_method = "all"          # TODO
        label = "WT" + self.call_number   # TODO

        cleaning_algorithm.label = label

        output_file_path = "score_wavelets_optim_{}.json".format(self.call_number)

        cleaning_algorithm = WaveletTransform()

        output_dict = cleaning_algorithm.run(cleaning_function_params,
                                             input_file_or_dir_path_list,
                                             benchmark_method,
                                             output_file_path,
                                             plot=False,
                                             saveplot=False)

        # Convert output_dict to error (e.g. compute the mean delta_psi per range of energy)
        print(output_dict)
        error = None      # TODO

        return error

