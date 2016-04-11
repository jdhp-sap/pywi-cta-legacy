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
This module contains unit tests for the "denoising.tailcut" module.
"""

import denoising_with_tailcut as tailcut       # TODO

import numpy as np

import unittest

class TestTailcut(unittest.TestCase):
    """
    Contains unit tests for the "denoising.tailcut" module.
    """

    # Test the "tailcut" function #############################################

    def test_example1(self):
        """Check the output of the tailcut function."""

        # Input image #################

        # [[  0   0   0   0   0   0]
        #  [128 128 128 128 128 128]
        #  [128  64 192 192  64 128]
        #  [128  64 192 192  64 128]
        #  [128 128 128 128 128 128]
        #  [  0   0   0   0   0   0]]

        input_img = np.zeros([6, 6], dtype=np.uint8)
        input_img[1:5, :] = 128   # 0.5
        input_img[2:4, 1:5] = 64    # 0.25
        input_img[2:4, 2:4] = 192   # 0.75

        # Output image ################

        output_img = tailcut.tailcut(input_img,
                                     high_threshold=0.7,
                                     low_threshold=0.4)

        # Expected output image #######

        # [[  0   0   0   0   0   0]
        #  [  0 128 128 128 128   0]
        #  [  0   0 192 192   0   0]
        #  [  0   0 192 192   0   0]
        #  [  0 128 128 128 128   0]
        #  [  0   0   0   0   0   0]]

        expected_output_img = np.zeros([6, 6], dtype=np.uint8)
        expected_output_img[1:5, 1:5] = 128   # 0.5
        expected_output_img[2:4, 1:5] = 0
        expected_output_img[2:4, 2:4] = 192   # 0.75

        np.testing.assert_array_equal(output_img, expected_output_img)

    def test_example2(self):
        """Check the output of the tailcut function."""

        # Input image #################

        # [[  0   0   0   0   0   0   0]
        #  [ 64  64 128 128 128  64  64]
        #  [ 64 192 128 128 128 192  64]
        #  [ 64  64 128 128 128  64  64]
        #  [  0   0   0   0   0   0   0]]

        input_img = np.zeros([5, 7], dtype=np.uint8)
        input_img[1:4, :] = 64   # 0.25
        input_img[1:4, 2:5] = 128   # 0.5
        input_img[2, 1] = 192   # 0.75
        input_img[2, 5] = 192   # 0.75

        # Output image ################

        output_img = tailcut.tailcut(input_img,
                                     high_threshold=0.7,
                                     low_threshold=0.4)

        # Expected output image #######

        # [[  0   0   0   0   0   0   0]
        #  [  0   0 128   0 128   0   0]
        #  [  0 192 128   0 128 192   0]
        #  [  0   0 128   0 128   0   0]
        #  [  0   0   0   0   0   0   0]]

        expected_output_img = np.zeros([5, 7], dtype=np.uint8)
        expected_output_img[1:4, 2] = 128   # 0.5
        expected_output_img[1:4, 4] = 128   # 0.5
        expected_output_img[2, 1] = 192   # 0.75
        expected_output_img[2, 5] = 192   # 0.75

        np.testing.assert_array_equal(output_img, expected_output_img)
    

if __name__ == '__main__':
    unittest.main()

