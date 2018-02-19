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

__all__ = ['get_islands',
           'kill_isolated_pixels',
           'kill_isolated_pixels_stats',
           'number_of_islands']

import numpy as np
import scipy.ndimage as ndimage

# See: https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html


def get_islands(array, threshold=0.2):
    """
    ...

    Parameters
    ----------
    array : Numpy array
        The input image to clean.
    threshold : float
        The "level of the sea" before island cleaning.

    Returns
    -------
    Numpy array
        ``filtered_array`` the input image with all pixels below ``threshold`` put to 0 (may contain NaN values).

    Numpy array
        ``label_array`` define the island id each pixel belongs to (doesn't contain NaN values).

    Integer
        ``num_labels`` the number of islands.
    """

    array = array.astype('float64', copy=True)
    filtered_array = np.copy(array)

    # Put NaN pixels to 0
    # This is OK as long as it is made temporary and internally to avoid issues
    # with scipy
    filtered_array[np.isnan(filtered_array)] = 0.

    # Put to 0 pixels that are below 'threshold'
    if threshold is not None:
        filtered_array[filtered_array < threshold] = 0.
    mask = filtered_array > 0

    # Detect islands ("label")
    label_array, num_labels = ndimage.label(mask)#, structure=np.ones((5, 5)))

    # Put back NaN in filtered_array (required to avoid bugs in others
    # functions (e.g. uncoherent dimensions with pixels_positions).
    filtered_array[np.isnan(array)] = np.nan

    return filtered_array, label_array, num_labels


def kill_isolated_pixels(array, threshold=0.2):
    """
    ...

    Parameters
    ----------
    array : Numpy array
        The input image to clean.
    threshold : float
        The "level of the sea" before island cleaning.

    Returns
    -------
    Numpy array
        The input image ``array`` with isolated islands removed.
        Only keeping the biggest islands (the largest surface).
    """

    array = array.astype('float64', copy=True)
    filtered_array, label_array, num_labels = get_islands(array, threshold)

    # Put NaN pixels to 0
    # This is OK as long as it is made temporary and internally to avoid issues
    # with scipy
    filtered_array[np.isnan(filtered_array)] = 0.

    # Count the number of pixels for each island
    num_pixels_per_island = ndimage.sum(filtered_array, label_array, range(num_labels + 1))

    # Only keep the biggest island
    mask_biggest_island = num_pixels_per_island < np.max(num_pixels_per_island)
    remove_pixel = mask_biggest_island[label_array]

    filtered_array[remove_pixel] = 0

    # Put back NaN in filtered_array (required to avoid bugs in others
    # functions (e.g. uncoherent dimensions with pixels_positions).
    filtered_array[np.isnan(array)] = np.nan

    return filtered_array


def kill_isolated_pixels_stats(array, threshold=0.2):

    array = array.astype('float64', copy=True)
    filtered_array = kill_isolated_pixels(array, threshold=threshold)

    delta_pe = np.nansum(array - filtered_array)
    delta_abs_pe = np.nansum(np.abs(array - filtered_array))


    array[np.isfinite(array) & (array != 0)] = 1                              # May genereate warnings on NaN values
    filtered_array[np.isfinite(filtered_array) & (filtered_array != 0)] = 1   # May genereate warnings on NaN values

    delta_num_pixels = np.nansum(array - filtered_array)

    return float(delta_pe), float(delta_abs_pe), float(delta_num_pixels)


def number_of_islands(array, threshold=0.2):
    filtered_array, label_array, num_labels = get_islands(array, threshold)
    return num_labels

