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
... TODO
"""

__all__ = ['astry_to_2d_array',
           'astry_to_3d_array']

import numpy as np

def astry_to_2d_array(input_img, crop=False):
    if crop:
        return astry_to_2d_array_crop(input_img)
    else:
        return astry_to_2d_array_no_crop(input_img)


def astry_to_2d_array_no_crop(input_img):
    """
    Crop images comming form "ASTRI" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    # Check the image
    if len(input_img) != (37*64):
        raise ValueError("The input image is not a valide ASTRI telescope image.")

    input_img_ext = np.zeros(input_img.shape[0] + 1)
    input_img_ext[:-1] = input_img[:]
    input_img_ext[-1] = np.nan

    # Make the transformation map
    img_map = np.zeros([8*7, 8*7], dtype=int)
    img_map[:] = -1

    img_map[0*8:1*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 34 * 64
    img_map[0*8:1*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 35 * 64
    img_map[0*8:1*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 36 * 64

    img_map[1*8:2*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 29 * 64
    img_map[1*8:2*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 30 * 64
    img_map[1*8:2*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 31 * 64
    img_map[1*8:2*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 32 * 64
    img_map[1*8:2*8, 5*8:6*8] = np.arange(64).reshape([8,8])[::-1,:] + 33 * 64

    img_map[2*8:3*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 22 * 64
    img_map[2*8:3*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 23 * 64
    img_map[2*8:3*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 24 * 64
    img_map[2*8:3*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 25 * 64
    img_map[2*8:3*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 26 * 64
    img_map[2*8:3*8, 5*8:6*8] = np.arange(64).reshape([8,8])[::-1,:] + 27 * 64
    img_map[2*8:3*8, 6*8:7*8] = np.arange(64).reshape([8,8])[::-1,:] + 28 * 64

    img_map[3*8:4*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 15 * 64
    img_map[3*8:4*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 16 * 64
    img_map[3*8:4*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 17 * 64
    img_map[3*8:4*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 18 * 64
    img_map[3*8:4*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 19 * 64
    img_map[3*8:4*8, 5*8:6*8] = np.arange(64).reshape([8,8])[::-1,:] + 20 * 64
    img_map[3*8:4*8, 6*8:7*8] = np.arange(64).reshape([8,8])[::-1,:] + 21 * 64

    img_map[4*8:5*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  8 * 64
    img_map[4*8:5*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  9 * 64
    img_map[4*8:5*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 10 * 64
    img_map[4*8:5*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 11 * 64
    img_map[4*8:5*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 12 * 64
    img_map[4*8:5*8, 5*8:6*8] = np.arange(64).reshape([8,8])[::-1,:] + 13 * 64
    img_map[4*8:5*8, 6*8:7*8] = np.arange(64).reshape([8,8])[::-1,:] + 14 * 64

    img_map[5*8:6*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  3 * 64
    img_map[5*8:6*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  4 * 64
    img_map[5*8:6*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  5 * 64
    img_map[5*8:6*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  6 * 64
    img_map[5*8:6*8, 5*8:6*8] = np.arange(64).reshape([8,8])[::-1,:] +  7 * 64

    img_map[6*8:7*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  0 * 64
    img_map[6*8:7*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  1 * 64
    img_map[6*8:7*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  2 * 64

    # Make the output image
    cropped_img = input_img_ext[[img_map.ravel()]].reshape([8*7, 8*7])

    return cropped_img


def astry_to_2d_array_crop(input_img):
    """
    Crop images comming form "ASTRI" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    # Check the image
    if len(input_img) != (37*64):
        raise ValueError("The input image is not a valide ASTRI telescope image.")

    # Make the transformation map
    img_map = np.zeros([8*5, 8*5], dtype=int)

    img_map[0*8:1*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 29 * 64
    img_map[0*8:1*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 30 * 64
    img_map[0*8:1*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 31 * 64
    img_map[0*8:1*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 32 * 64
    img_map[0*8:1*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 33 * 64

    img_map[1*8:2*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 23 * 64
    img_map[1*8:2*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 24 * 64
    img_map[1*8:2*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 25 * 64
    img_map[1*8:2*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 26 * 64
    img_map[1*8:2*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 27 * 64

    img_map[2*8:3*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 16 * 64
    img_map[2*8:3*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 17 * 64
    img_map[2*8:3*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 18 * 64
    img_map[2*8:3*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 19 * 64
    img_map[2*8:3*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 20 * 64

    img_map[3*8:4*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  9 * 64
    img_map[3*8:4*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 10 * 64
    img_map[3*8:4*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 11 * 64
    img_map[3*8:4*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 12 * 64
    img_map[3*8:4*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 13 * 64

    img_map[4*8:5*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  3 * 64
    img_map[4*8:5*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  4 * 64
    img_map[4*8:5*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  5 * 64
    img_map[4*8:5*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  6 * 64
    img_map[4*8:5*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  7 * 64

    # Make the output image
    cropped_img = input_img[[img_map.ravel()]].reshape([8*5, 8*5])

    return cropped_img


def astry_to_3d_array(input_img, crop=False):
    """
    Crop images comming form "ASTRI" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    # Check the image
    if input_img.shape[1] != (37*64):
        raise ValueError("The input image is not a valide ASTRI telescope image.")

    cropped_img_list = []

    for img_2d in input_img:
        cropped_img_list.append(astry_to_2d_array(img_2d, crop))

    return np.array(cropped_img_list)



def astry_pixel_mask(crop=False):
    """
    """

    if crop:
        img_mask = np.ones([8*5, 8*5], dtype=int)
    else:
        img_mask = np.zeros([8*7, 8*7], dtype=int)

        img_mask[0*8:1*8, 2*8:3*8] = 1
        img_mask[0*8:1*8, 3*8:4*8] = 1
        img_mask[0*8:1*8, 4*8:5*8] = 1

        img_mask[1*8:2*8, 1*8:2*8] = 1
        img_mask[1*8:2*8, 2*8:3*8] = 1
        img_mask[1*8:2*8, 3*8:4*8] = 1
        img_mask[1*8:2*8, 4*8:5*8] = 1
        img_mask[1*8:2*8, 5*8:6*8] = 1

        img_mask[2*8:3*8, 0*8:1*8] = 1
        img_mask[2*8:3*8, 1*8:2*8] = 1
        img_mask[2*8:3*8, 2*8:3*8] = 1
        img_mask[2*8:3*8, 3*8:4*8] = 1
        img_mask[2*8:3*8, 4*8:5*8] = 1
        img_mask[2*8:3*8, 5*8:6*8] = 1
        img_mask[2*8:3*8, 6*8:7*8] = 1

        img_mask[3*8:4*8, 0*8:1*8] = 1
        img_mask[3*8:4*8, 1*8:2*8] = 1
        img_mask[3*8:4*8, 2*8:3*8] = 1
        img_mask[3*8:4*8, 3*8:4*8] = 1
        img_mask[3*8:4*8, 4*8:5*8] = 1
        img_mask[3*8:4*8, 5*8:6*8] = 1
        img_mask[3*8:4*8, 6*8:7*8] = 1

        img_mask[4*8:5*8, 0*8:1*8] = 1
        img_mask[4*8:5*8, 1*8:2*8] = 1
        img_mask[4*8:5*8, 2*8:3*8] = 1
        img_mask[4*8:5*8, 3*8:4*8] = 1
        img_mask[4*8:5*8, 4*8:5*8] = 1
        img_mask[4*8:5*8, 5*8:6*8] = 1
        img_mask[4*8:5*8, 6*8:7*8] = 1

        img_mask[5*8:6*8, 1*8:2*8] = 1
        img_mask[5*8:6*8, 2*8:3*8] = 1
        img_mask[5*8:6*8, 3*8:4*8] = 1
        img_mask[5*8:6*8, 4*8:5*8] = 1
        img_mask[5*8:6*8, 5*8:6*8] = 1

        img_mask[6*8:7*8, 2*8:3*8] = 1
        img_mask[6*8:7*8, 3*8:4*8] = 1
        img_mask[6*8:7*8, 4*8:5*8] = 1

    return img_mask
