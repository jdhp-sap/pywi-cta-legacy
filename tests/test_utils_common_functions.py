#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

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
This module contains unit tests for the "common_functions" module.
"""

import sys
sys.path.append("utils")
import common_functions as common

import copy
import numpy as np

import unittest

class TestCommonFunctions(unittest.TestCase):
    """
    Contains unit tests for the "common_functions" module.
    """

    # Test the "extract_min" function ###############################

    def test_extract_min_ex1(self):

        # Make image ##################

        a1 = np.array([[  2., 0., -1. ],
                       [ 10., 0.,  3. ]])

        a2 = np.array([[  2., 0., -2. ],
                       [ 30., 0.,  3. ]])

        a3 = np.array([[  2., 0., -1. ],
                       [ 10., 0.,  3. ]])

        min_value = common.extract_min([a1, a2, a3])

        # Check result ################

        self.assertEqual(min_value, -2.)


    def test_extract_min_ex_nan(self):

        # Make image ##################

        a1 = np.array([[ np.nan,     0.,    -1. ],
                       [    10., np.nan,     3. ]])

        a2 = np.array([[     2., np.nan,    -2. ],
                       [    30.,     0., np.nan ]])

        a3 = np.array([[ np.nan,     0.,    -1. ],
                       [    10., np.nan,     3. ]])

        min_value = common.extract_min([a1, a2, a3])

        # Check result ################

        self.assertEqual(min_value, -2.)


    # Test the "extract_max" function ###############################

    def test_extract_max_ex1(self):

        # Make image ##################

        a1 = np.array([[  2., 0., -1. ],
                       [ 10., 0.,  3. ]])

        a2 = np.array([[  2., 0., -2. ],
                       [ 30., 0.,  3. ]])

        a3 = np.array([[  2., 0., -1. ],
                       [ 10., 0.,  3. ]])

        max_value = common.extract_max([a1, a2, a3])

        # Check result ################

        self.assertEqual(max_value, 30.)


    def test_extract_max_ex_nan(self):

        # Make image ##################

        a1 = np.array([[ np.nan,     0.,    -1. ],
                       [    10., np.nan,     3. ]])

        a2 = np.array([[     2., np.nan,    -2. ],
                       [    30.,     0., np.nan ]])

        a3 = np.array([[ np.nan,     0.,    -1. ],
                       [    10., np.nan,     3. ]])

        max_value = common.extract_max([a1, a2, a3])

        # Check result ################

        self.assertEqual(max_value, 30.)

if __name__ == '__main__':
    unittest.main()

