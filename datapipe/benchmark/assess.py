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

__all__ = ['normalize',
           'assess_image_cleaning_meth1',
           'assess_image_cleaning_meth2']

import numpy as np

def normalize(input_array):
    output_array = (input_array - input_array.min()) / (input_array.max() - input_array.min())
    return output_array


def assess_image_cleaning_meth1(input_image, output_image, reference_image):
    """
    TODO...

    Parameters
    ----------
    input_image: 2D numpy.array
        The RAW original image.
    output_image: 2D numpy.array
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D numpy.array
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    The mark (float number) of the image cleaning algorithm for the given
    image.
    """
    
    mark = None

    normalized_diff_array = normalize(output_image) - normalize(reference_image)
    mark = np.mean(np.abs(normalized_diff_array))

    return mark


def assess_image_cleaning_meth2(input_image, output_image, reference_image):
    """
    TODO...

    Parameters
    ----------
    input_image: 2D numpy.array
        The RAW original image.
    output_image: 2D numpy.array
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D numpy.array
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    The mark (float number) of the image cleaning algorithm for the given
    image.
    """
    
    raise Exception("Not yet implemented")

