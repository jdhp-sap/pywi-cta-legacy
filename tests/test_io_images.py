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

from datapipe.io import images

import numpy as np
import os
import tempfile

import unittest

class TestImages(unittest.TestCase):
    """
    Contains unit tests for the "io.images" module.
    """

    # Test the "save" and "load" functions ####################################

    def test_load_and_save(self):
        """Check the `images.load` and `images.save` functions."""

        img = np.random.randint(128, size=(4, 6))

        # Make a temporary directory to store fits files
        with tempfile.TemporaryDirectory() as temp_dir_path:

            img_path = os.path.join(temp_dir_path, "test.fits")

            # Save the image
            images.save(img, img_path)

            # Load the saved image
            loaded_img = images.load(img_path, 0)

            # Check img vs loaded_img
            np.testing.assert_array_equal(img, loaded_img)
    
        # The temporary directory and all its contents are removed now


    # Test the "save" function exceptions #####################################

    def test_save_wrong_dimension_error(self):
        """Check the call to `images.load` fails with an WrongDimensionError
        when saved images have more than 3 dimensions or less than 2
        dimensions."""

        img_1d = np.random.randint(128, size=(3))           # Make a 1D image
        img_2d = np.random.randint(128, size=(3, 3))        # Make a 2D image
        img_3d = np.random.randint(128, size=(3, 3, 3))     # Make a 3D image
        img_4d = np.random.randint(128, size=(3, 3, 3, 3))  # Make a 4D image

        # Make a temporary directory to store fits files
        with tempfile.TemporaryDirectory() as temp_dir_path:

            img_path = os.path.join(temp_dir_path, "test.fits")

            # Save the 1D image (should raise an exception)
            with self.assertRaises(images.WrongDimensionError):
                images.save(img_1d, img_path)

            # Save the 2D image (should not raise any exception)
            try:
                images.save(img_2d, img_path)
            except images.WrongDimensionError:
                self.fail("images.save() raised WrongDimensionError unexpectedly!")

            # Save the 3D image (should not raise any exception)
            try:
                images.save(img_3d, img_path)
            except images.WrongDimensionError:
                self.fail("images.save() raised WrongDimensionError unexpectedly!")

            # Save the 4D image (should raise an exception)
            with self.assertRaises(images.WrongDimensionError):
                images.save(img_4d, img_path)

        # The temporary directory and all its contents are removed now


    # Test the "load" function exceptions #####################################

    def test_load_wrong_hdu_error(self):
        """Check the call to `images.load` fails with an WrongDimensionError
        when saved images have more than 3 dimensions or less than 2
        dimensions."""

        img = np.random.randint(128, size=(3, 3))        # Make a 2D image

        # Make a temporary directory to store fits files
        with tempfile.TemporaryDirectory() as temp_dir_path:

            img_path = os.path.join(temp_dir_path, "test.fits")

            # Save the image
            images.save(img, img_path)

            # Load the saved image (should raise an exception)
            with self.assertRaises(images.WrongHDUError):
                loaded_img = images.load(img_path, hdu_index=1000)

            # Load the saved image (should not raise any exception)
            try:
                loaded_img = images.load(img_path, hdu_index=0)
            except images.WrongHDUError:
                self.fail("images.load() raised WrongHDUError unexpectedly!")

        # The temporary directory and all its contents are removed now


if __name__ == '__main__':
    unittest.main()

