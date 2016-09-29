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
           'list_assess_methods',
           'assess_image_cleaning']

import numpy as np
from astropy.units import Quantity
import astropy.units as u

import sys


# EXCEPTIONS #################################################################

class AssessError(Exception):
    pass

class UnknownMethod(AssessError):
    pass

class EmptyOutputImageError(AssessError):
    """
    Exception raised when the output image only have null pixels (to prevent
    division by 0 in the assess function).
    """

    def __init__(self):
        super(EmptyOutputImageError, self).__init__("Empty output image error")

class EmptyReferenceImageError(AssessError):
    """
    Exception raised when the reference image only have null pixels (to prevent
    division by 0 in the assess function).
    """

    def __init__(self):
        super(EmptyReferenceImageError, self).__init__("Empty reference image error")


# ASSESS FUNCTIONS ###########################################################

# Mean Pixel Difference with Normalization (mpd)

def normalize(input_array):
    """Normalize the given image such that its pixels value fit between 0.0 and
    1.0.

    Parameters
    ----------
    image : Numpy array
        The image to normalize (whatever its shape)

    Returns
    -------
    output_array : Numpy array
        The normalized version of the input image (keeping the same dimension
        and shape)
    """
    output_array = (input_array - input_array.min()) / (input_array.max() - input_array.min())
    return output_array

def assess_image_cleaning_meth1(input_img, output_image, reference_image, params=None):
    """
    TODO...

    Parameters
    ----------
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
    
    if (params is not None) and ('normalize_images' in params) and (params['normalize_images']):
        normalized_diff_array = normalize(output_image) - normalize(reference_image)
        mark = np.mean(np.abs(normalized_diff_array))
    else:
        diff_array = output_image - reference_image
        mark = np.mean(np.abs(diff_array))

    return (mark,)


# Mean Pixel Difference + Total PhotoElectron Difference (mpdspd)

def assess_image_cleaning_meth2(input_img, output_image, reference_image, params=None):
    """
    TODO...

    Parameters
    ----------
    output_image: 2D numpy.array
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D numpy.array
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    mark : 1D Numpy array containing float numbers
        The mark (float number) of the image cleaning algorithm for the given
        image.
    """
    
    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if sum_output_image <= 0:                 # TODO
        raise EmptyOutputImageError()

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark1 = np.mean(np.abs((output_image / sum_output_image) - (reference_image / sum_reference_image)))
    mark2 = np.abs(sum_output_image - sum_reference_image) / sum_reference_image

    return (mark1, mark2)


# Signed Total PhotoElectron Difference (sspd)

def assess_image_cleaning_meth3(input_img, output_image, reference_image, params=None):
    """
    TODO...

    Parameters
    ----------
    output_image: 2D numpy.array
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D numpy.array
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    mark : 1D Numpy array containing float numbers
        The mark (float number) of the image cleaning algorithm for the given
        image.
    """
    
    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if sum_output_image <= 0:                 # TODO
        raise EmptyOutputImageError()

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = (sum_output_image - sum_reference_image) / sum_reference_image

    return (mark,)


# ASSESS FUNCTIONS DRIVER ####################################################

METHOD_DICT = {
    "mpd":    assess_image_cleaning_meth1,
    "mpdspd": assess_image_cleaning_meth2,
    "sspd":   assess_image_cleaning_meth3
}

def assess_image_cleaning(input_img, output_img, reference_img, benchmark_method, params=None):
    """TODO...

    Parameters
    ----------
    input_img: 2D numpy.array
        The RAW original image.
    output_img: 2D numpy.array
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_img: 2D numpy.array
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    mark : a tuple of float numbers
        The mark (may be multivalued) of the image cleaning algorithm for the
        given image.
    """

    try:
        score_tuple = METHOD_DICT[benchmark_method](input_img, output_img, reference_img, params)
    except KeyError:
        raise UnknownMethod()

    return score_tuple

def list_assess_methods():
    """TODO...
    """

    return METHOD_DICT.keys()

