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
           'assess_image_cleaning_meth1bis',
           'assess_image_cleaning_meth2']

import numpy as np
from astropy.units import Quantity
import astropy.units as u


def normalize(input_array):
    output_array = (input_array - input_array.min()) / (input_array.max() - input_array.min())
    return output_array


def hillas_parameters(image):
    """Compute Hillas parameters for a given shower image.

    Taken from ctapipe (ctapipe/reco/hillas.py)

    Reference: Appendix of the Whipple Crab paper Weekes et al. (1998)
    http://adsabs.harvard.edu/abs/1989ApJ...342..379W
    (corrected for some obvious typos)

    Parameters
    ----------
    image : 2D Numpy array
        Pixel values corresponding

    Returns
    -------
    hillas_parameters : 1D Numpy array
    """

    raise Exception("Not yet implemented")

    ## pix_x : array_like Pixel x-coordinate
    #pix_x = Quantity(np.asanyarray(pix_x, dtype=np.float64)).value
    ## pix_y : array_like Pixel y-coordinate
    #pix_y = Quantity(np.asanyarray(pix_y, dtype=np.float64)).value
    #image = np.asanyarray(image, dtype=np.float64)

    #image_size = 1.  # TODO

    num_x, num_y = image.shape[0], image.shape[1]
    x = np.linspace(-0.2, 0.2, num_x)   # TODO
    y = np.linspace(-0.2, 0.2, num_y)   # TODO
    xv, yv = np.meshgrid(x, y)

    pix_x = xv.ravel()
    pix_y = xv.ravel()

    image = image.ravel()  # 2D -> 1D

    pix_x = Quantity(np.asanyarray(pix_x, dtype=np.float64)).value  # TODO
    pix_y = Quantity(np.asanyarray(pix_y, dtype=np.float64)).value  # TODO
    image = np.asanyarray(image, dtype=np.float64)                  # TODO

    assert pix_x.shape == image.shape
    assert pix_y.shape == image.shape

    # Compute image moments
    size = np.sum(image)
    center_x = np.sum(image * pix_x) / size
    center_y = np.sum(image * pix_y) / size
    m_xx = np.sum(image * pix_x * pix_x) / size  # note: typo in paper
    m_yy = np.sum(image * pix_y * pix_y) / size
    m_xy = np.sum(image * pix_x * pix_y) / size  # note: typo in paper

    # Compute major axis line representation y = a * x + b
    S_xx = m_xx - center_x * center_x
    S_yy = m_yy - center_y * center_y
    S_xy = m_xy - center_x * center_y
    d = S_yy - S_xx
    temp = d * d + 4 * S_xy * S_xy
    a = (d + np.sqrt(temp)) / (2 * S_xy)
    b = center_y - a * center_x

    # Compute Hillas parameters
    width_2 = (S_yy + a * a * S_xx - 2 * a * S_xy) / (1 + a * a)
    width = np.sqrt(width_2)
    length_2 = (S_xx + a * a * S_yy + 2 * a * S_xy) / (1 + a * a)
    length = np.sqrt(length_2)
    miss = np.abs(b / (1 + a * a))
    r = np.sqrt(center_x * center_x + center_y * center_y)
    phi = np.arctan2(center_y, center_x)

    # Compute azwidth by transforming to (p, q) coordinates
    sin_theta = center_y / r
    cos_theta = center_x / r
    q = (center_x - pix_x) * sin_theta + (pix_y - center_y) * cos_theta
    m_q = np.sum(image * q) / size
    m_qq = np.sum(image * q * q) / size
    azwidth_2 = m_qq - m_q * m_q
    azwidth = np.sqrt(azwidth_2)

    #return [size, center_x, center_y, length, width, r, phi, psi=None, miss]
    return np.array([size, center_x, center_y, length, width, r, phi, miss])


def assess_image_cleaning_meth1(input_image, output_image, reference_image, normalize_images=True):
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

    if normalize_images:
        normalized_diff_array = normalize(output_image) - normalize(reference_image)
        mark = np.mean(np.abs(normalized_diff_array))
    else:
        diff_array = output_image - reference_image
        mark = np.mean(np.abs(diff_array))

    return mark


def assess_image_cleaning_meth1bis(input_image, output_image, reference_image):
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

    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if (sum_output_image > 0) and (sum_reference_image > 0):
        mark1 = np.mean(np.abs((output_image / sum_output_image) - (reference_image / sum_reference_image)))
        mark2 = np.abs(sum_output_image - sum_reference_image) / (reference_image / sum_reference_image)
        mark = (mark1, mark2)

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
    
    hillas_out = hillas_parameters(output_image)
    hillas_ref = hillas_parameters(reference_image)

    print(hillas_ref)

    return np.abs(hillas_out - hillas_ref)


