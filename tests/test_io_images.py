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
This module contains unit tests for the "io.images" module.
"""

import utils as images       # TODO

import os
import numpy as np

import unittest

class TestImages(unittest.TestCase):
    """
    Contains unit tests for the "io.images" module.
    """

    # Test the "load" function ################################################

    def test_png(self):
        """Check the output of the "load" function."""

        current_package_path = os.path.dirname(__file__)
        img_path = os.path.join(current_package_path, "data", "test.png")

        # Loaded image ################

        img = images.load(img_path)

        # Expected image ##############

        # [[  0   0   0   0   0   0]
        #  [  0 128 128 128 128   0]
        #  [  0 128 255 255 128   0]
        #  [  0 128 255 255 128   0]
        #  [  0 128 128 128 128   0]
        #  [  0   0   0   0   0   0]]

        expected_img = np.zeros([6, 6], dtype=np.uint8)
        expected_img[1:5, 1:5] = 128
        expected_img[2:4, 2:4] = 255

        np.testing.assert_array_equal(img, expected_img)
    

if __name__ == '__main__':
    unittest.main()

