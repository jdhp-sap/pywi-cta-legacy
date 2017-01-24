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

__all__ = ['kill_isolated_pixels']

import numpy as np
import scipy.ndimage as ndimage

# See: https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html

def kill_isolated_pixels(array, threshold=0.2, plot=False):
    """
    Return array with isolated islands removed.
    Only keeping the biggest islands (largest surface).

    :param array: Array with completely isolated cells
    :param struct: Structure array for generating unique regions
    :return: Filtered array with just the largest island 
    """

    filtered_array = np.copy(array)

    # Put to 0 pixels that are below 'threshold'
    filtered_array[filtered_array < threshold] = 0
    mask = filtered_array > 0

    # Detect islands ("label")
    label_array, num_labels = ndimage.label(mask)#, structure=np.ones((5, 5)))

    # Count the number of pixels for each island
    num_pixels_per_island = ndimage.sum(filtered_array, label_array, range(num_labels + 1))

    # Only keep the biggest island
    mask_biggest_island = num_pixels_per_island < np.max(num_pixels_per_island)
    remove_pixel = mask_biggest_island[label_array]

    filtered_array[remove_pixel] = 0

    return filtered_array
