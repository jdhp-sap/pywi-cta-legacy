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
This module contains unit tests for the "image.hillas_parameters" module.
"""

from datapipe.image.hillas_parameters import get_hillas_parameters

import copy
import numpy as np

import unittest

class TestHillasParameters(unittest.TestCase):
    """
    Contains unit tests for the "image.hillas_parameters" module.
    """

    # Test the "get_hillas_parameters" function ###############################

    def test_get_hillas_parameters1_nan(self):

        # Make image ##################

        img = np.array([[ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  1., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  3., 1., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  6., 11., 2., 0., 0., 0.],
                        [ 0., 0., 0.,  0., 30., 14., 3., 1., 0., 0.],
                        [ 0., 0., 0.,  3., 13.,  9., 4., 0., 0., 0.],
                        [ 0., 0., 0., 17., 16.,  3., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  2.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.]])

        img_nan = np.copy(img)
        lx, ly = img_nan.shape
        img_nan[0:2,0:2] = np.nan
        img_nan[0:2,-2:ly] = np.nan
        img_nan[-2:lx,0:2] = np.nan
        img_nan[-2:lx,-2:ly] = np.nan

        # Hillas

        hillas = get_hillas_parameters(img, implementation=1)
        hillas_nan = get_hillas_parameters(img_nan, implementation=1)

        # Check results

        #self.assertEqual(hillas, hillas_nan)

        for param, param_nan in zip(hillas, hillas_nan):
            try:
                value = param.value
                value_nan = param_nan.value
            except:
                value = param
                value_nan = param_nan
            
            np.testing.assert_almost_equal(value, value_nan, decimal=10)


    def test_get_hillas_parameters2_nan(self):

        # Make image ##################

        img = np.array([[ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  1., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  3., 1., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  6., 11., 2., 0., 0., 0.],
                        [ 0., 0., 0.,  0., 30., 14., 3., 1., 0., 0.],
                        [ 0., 0., 0.,  3., 13.,  9., 4., 0., 0., 0.],
                        [ 0., 0., 0., 17., 16.,  3., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  2.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.]])

        img_nan = np.copy(img)
        lx, ly = img_nan.shape
        img_nan[0:2,0:2] = np.nan
        img_nan[0:2,-2:ly] = np.nan
        img_nan[-2:lx,0:2] = np.nan
        img_nan[-2:lx,-2:ly] = np.nan

        # Hillas

        hillas = get_hillas_parameters(img, implementation=2)
        hillas_nan = get_hillas_parameters(img_nan, implementation=2)

        # Check results

        self.assertEqual(hillas, hillas_nan)


    def test_get_hillas_parameters1_nan_with_pix_pos(self):

        # Make image ##################

        img = np.array([[ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  1., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  3., 1., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  6., 11., 2., 0., 0., 0.],
                        [ 0., 0., 0.,  0., 30., 14., 3., 1., 0., 0.],
                        [ 0., 0., 0.,  3., 13.,  9., 4., 0., 0., 0.],
                        [ 0., 0., 0., 17., 16.,  3., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  2.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.]])

        img_nan = np.copy(img)
        lx, ly = img_nan.shape
        img_nan[0:2,0:2] = np.nan
        img_nan[0:2,-2:ly] = np.nan
        img_nan[-2:lx,0:2] = np.nan
        img_nan[-2:lx,-2:ly] = np.nan

        pix_pos = (np.array([[-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543]]),
                   np.array([[ 0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181],
                             [ 0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543],
                             [ 0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905],
                             [ 0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267],
                             [ 0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125],
                             [ 0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375],
                             [ 0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625],
                             [ 0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875],
                             [-0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875]]))

        pix_pos_nan = copy.deepcopy(pix_pos)

        lx, ly = pix_pos_nan[0].shape

        pix_pos_nan[0][0:2,0:2] = np.nan
        pix_pos_nan[0][0:2,-2:ly] = np.nan
        pix_pos_nan[0][-2:lx,0:2] = np.nan
        pix_pos_nan[0][-2:lx,-2:ly] = np.nan

        pix_pos_nan[1][0:2,0:2] = np.nan
        pix_pos_nan[1][0:2,-2:ly] = np.nan
        pix_pos_nan[1][-2:lx,0:2] = np.nan
        pix_pos_nan[1][-2:lx,-2:ly] = np.nan

        # Hillas
        hillas = get_hillas_parameters(img, implementation=1, pixels_position=pix_pos)
        hillas_nan = get_hillas_parameters(img_nan, implementation=1, pixels_position=pix_pos_nan)

        # Check results

        #self.assertEqual(hillas, hillas_nan)

        for param, param_nan in zip(hillas, hillas_nan):
            try:
                value = param.value
                value_nan = param_nan.value
            except:
                value = param
                value_nan = param_nan
        
            np.testing.assert_almost_equal(value, value_nan, decimal=10)


    def test_get_hillas_parameters2_nan_with_pix_pos(self):

        # Make image ##################

        img = np.array([[ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  1., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  3., 1., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  6., 11., 2., 0., 0., 0.],
                        [ 0., 0., 0.,  0., 30., 14., 3., 1., 0., 0.],
                        [ 0., 0., 0.,  3., 13.,  9., 4., 0., 0., 0.],
                        [ 0., 0., 0., 17., 16.,  3., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  2.,  0.,  0., 0., 0., 0., 0.],
                        [ 0., 0., 0.,  0.,  0.,  0., 0., 0., 0., 0.]])

        img_nan = np.copy(img)
        lx, ly = img_nan.shape
        img_nan[0:2,0:2] = np.nan
        img_nan[0:2,-2:ly] = np.nan
        img_nan[-2:lx,0:2] = np.nan
        img_nan[-2:lx,-2:ly] = np.nan

        pix_pos = (np.array([[-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543],
                             [-0.0179375, -0.0107625, -0.0035875,  0.0035875,  0.0107625,  0.0179375,  0.0251125,  0.0337267,  0.0408905,  0.0480543]]),
                   np.array([[ 0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181,  0.0552181],
                             [ 0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543,  0.0480543],
                             [ 0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905,  0.0408905],
                             [ 0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267,  0.0337267],
                             [ 0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125,  0.0251125],
                             [ 0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375,  0.0179375],
                             [ 0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625,  0.0107625],
                             [ 0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875,  0.0035875],
                             [-0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875, -0.0035875]]))

        pix_pos_nan = copy.deepcopy(pix_pos)

        lx, ly = pix_pos_nan[0].shape

        pix_pos_nan[0][0:2,0:2] = np.nan
        pix_pos_nan[0][0:2,-2:ly] = np.nan
        pix_pos_nan[0][-2:lx,0:2] = np.nan
        pix_pos_nan[0][-2:lx,-2:ly] = np.nan

        pix_pos_nan[1][0:2,0:2] = np.nan
        pix_pos_nan[1][0:2,-2:ly] = np.nan
        pix_pos_nan[1][-2:lx,0:2] = np.nan
        pix_pos_nan[1][-2:lx,-2:ly] = np.nan

        # Hillas
        hillas = get_hillas_parameters(img, implementation=2, pixels_position=pix_pos)
        hillas_nan = get_hillas_parameters(img_nan, implementation=2, pixels_position=pix_pos_nan)

        # Check results

        #self.assertEqual(hillas, hillas_nan)

        for param, param_nan in zip(hillas, hillas_nan):
            try:
                value = param.value
                value_nan = param_nan.value
            except:
                value = param
                value_nan = param_nan
        
            np.testing.assert_almost_equal(value, value_nan, decimal=10)


if __name__ == '__main__':
    unittest.main()

