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
This module contains unit tests for the "benchmark.assess" module.
"""

from datapipe.benchmark import assess

import numpy as np

import unittest

class TestAssess(unittest.TestCase):
    """
    Contains unit tests for the "benchmark.assess" module.
    """

    # Test the "normalize" function ###########################################

    def test_normalize(self):
        """Check the output of the "normalize" function."""

        # Input image #################

        input_img = np.array([[1, 2, 2, 1],
                              [1, 3, 3, 1],
                              [1, 2, 2, 1]])

        # Expected output image #######

        expected_output_img = np.array([[0., 0.5, 0.5, 0.],
                                        [0., 1.0, 1.0, 0.],
                                        [0., 0.5, 0.5, 0.]])

        # Output image ################

        output_img = assess.normalize(input_img)

        # Test ########################

        np.testing.assert_array_equal(output_img, expected_output_img)


    # Test the "assess_image_cleaning_meth1bis" function ######################

    def test_assess_image_cleaning_meth1bis_input(self):
        """Check the input of the "assess_image_cleaning_meth1bis"
        function."""

        #######################################################################
        # Test 1: sum on output image is 0                                    #
        #######################################################################

        # Input image #################

        input_image = np.array([[1, 2, 2, 1],
                                [1, 3, 3, 1],
                                [1, 2, 2, 1]])

        # Output image ################

        output_image = np.array([[0, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]])

        # Reference image #############

        reference_image = np.array([[1, 2, 2, 1],
                                    [1, 3, 3, 1],
                                    [1, 2, 2, 1]])
    
        # Expected mark ###############

        expected_mark = None

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 2: sum on reference image is 0                                 #
        #######################################################################

        # Input image #################

        input_image = np.array([[1, 2, 2, 1],
                                [1, 3, 3, 1],
                                [1, 2, 2, 1]])

        # Output image ################

        output_image = np.array([[1, 2, 2, 1],
                                 [1, 3, 3, 1],
                                 [1, 2, 2, 1]])

        # Reference image #############

        reference_image = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]])
    
        # Expected mark ###############

        expected_mark = None

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 3: sum on output image is 0                                    #
        #######################################################################

        # Input image #################

        input_image = np.array([[1, 2, 2, 1],
                                [1, 3, 3, 1],
                                [1, 2, 2, 1]])

        # Output image ################

        output_image = np.array([[0., 0., 0., 0.],
                                 [0., 0., 0., 0.],
                                 [0., 0., 0., 0.]])

        # Reference image #############

        reference_image = np.array([[1, 2, 2, 1],
                                    [1, 3, 3, 1],
                                    [1, 2, 2, 1]])
    
        # Expected mark ###############

        expected_mark = None

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 4: sum on reference image is 0                                 #
        #######################################################################

        # Input image #################

        input_image = np.array([[1, 2, 2, 1],
                                [1, 3, 3, 1],
                                [1, 2, 2, 1]])

        # Output image ################

        output_image = np.array([[1, 2, 2, 1],
                                 [1, 3, 3, 1],
                                 [1, 2, 2, 1]])

        # Reference image #############

        reference_image = np.array([[0., 0., 0., 0.],
                                    [0., 0., 0., 0.],
                                    [0., 0., 0., 0.]])
    
        # Expected mark ###############

        expected_mark = None

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


    def test_assess_image_cleaning_meth1bis_output(self):
        """Check the output of the "assess_image_cleaning_meth1bis"
        function."""

        #######################################################################
        # Test 1: perfect output                                              #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[1, 2, 2, 1],
                                 [1, 3, 3, 1],
                                 [1, 2, 2, 1]])

        # Reference image #############

        reference_image = np.array([[1, 2, 2, 1],
                                    [1, 3, 3, 1],
                                    [1, 2, 2, 1]])
    
        # Expected mark ###############

        expected_mark = np.array([0., 0.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 2: perfect output                                              #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[.1, .2, .2, .1],
                                 [.1, .3, .3, .1],
                                 [.1, .2, .2, .1]])

        # Reference image #############

        reference_image = np.array([[.1, .2, .2, .1],
                                    [.1, .3, .3, .1],
                                    [.1, .2, .2, .1]])
    
        # Expected mark ###############

        expected_mark = np.array([0., 0.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 3: perfect shape but 10 time the energy                        #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[10., 20., 20., 10.],
                                 [10., 30., 30., 10.],
                                 [10., 20., 20., 10.]])

        # Reference image #############

        reference_image = np.array([[1., 2., 2., 1.],
                                    [1., 3., 3., 1.],
                                    [1., 2., 2., 1.]])
    
        # Expected mark ###############

        expected_mark = np.array([0., 9.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 4: perfect shape but the energy divided by 10                  #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[0.1, 0.2, 0.2, 0.1],
                                 [0.1, 0.3, 0.3, 0.1],
                                 [0.1, 0.2, 0.2, 0.1]])

        # Reference image #############

        reference_image = np.array([[1., 2., 2., 1.],
                                    [1., 3., 3., 1.],
                                    [1., 2., 2., 1.]])
    
        # Expected mark ###############

        expected_mark = np.array([0., 0.9])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 5: perfect energy but wrong shape                              #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[1., 1., 1., 1., 1.],
                                 [1., 1., 1., 1., 1.]])

        # Reference image #############

        reference_image = np.array([[1., 1., 1., 1., 2.],
                                    [1., 1., 1., 1., 0.]])
    
        # Expected mark ###############

        expected_mark = np.array([0.02, 0.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 6: perfect energy but wrong shape                              #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[1., 1., 1., 1., 1.],
                                 [1., 1., 1., 1., 1.]])

        # Reference image #############

        reference_image = np.array([[2., 2., 2., 2., 2.],
                                    [0., 0., 0., 0., 0.]])
    
        # Expected mark ###############

        expected_mark = np.array([0.1, 0.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_equal(mark, expected_mark)


        #######################################################################
        # Test 7: perfect energy but wrong shape                              #
        #######################################################################

        # Input image #################

        input_image = None

        # Output image ################

        output_image = np.array([[1., 1., 1., 1., 1.],
                                 [1., 1., 1., 1., 1.]])

        # Reference image #############

        reference_image = np.array([[1., 1., 1., 1., 1.5],
                                    [1., 1., 1., 1., 0.5]])
    
        # Expected mark ###############

        expected_mark = np.array([0.01, 0.])

        # Mark ########################

        mark = assess.assess_image_cleaning_meth1bis(input_image, output_image, reference_image)

        # Test ########################

        np.testing.assert_array_almost_equal(mark, expected_mark, decimal=10)
    

if __name__ == '__main__':
    unittest.main()

