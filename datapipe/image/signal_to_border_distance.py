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

__all__ = ['signal_to_border',
           'signal_to_border_distance',
           'pemax_on_border']

import math
import numpy as np

"""
Warning: so far, this module only works with "rectangular 2D images".
"""

def signal_to_border(img):
    """
    TODO
    """

    res = []

    # make a bigger array
    em = np.zeros(np.array(img.shape) + 2)
    em = em.astype("bool")
    em[1:-1,1:-1] = np.isfinite(img)

    while em.any():

        # Get the pixel sum of the shrinked image
        res.append(float(np.nansum(img[em[1:-1,1:-1]])))

        emt = em.copy()

        # "shrink" the "True" area in the mask by moving it in all directions, taking the logical 'AND'
        em[1:  ,1:]   &= emt[0:-1,0:-1]
        em[0:-1,0:-1] &= emt[1:,1:]
        em[1:  ,0:-1] &= emt[0:-1,1:]
        em[0:-1,1:]   &= emt[1:,0:-1]

        em[0:-1,:]    &= emt[1:  ,:]
        em[1:  ,:]    &= emt[0:-1,:]
        em[:   ,0:-1] &= emt[:   ,1:]
        em[:   ,1:]   &= emt[:   ,0:-1]

    return res


def signal_to_border_distance(img):
    """
    TODO
    """

    res = signal_to_border(img)

    sum_pe_img = res[0]

    dist = 0

    for pe in res[1:]:
        if pe == sum_pe_img:
            dist += 1
        else:
            break

    return dist


def pemax_on_border(img):
    """
    This function has been written to test the following rejection criterion:
    https://github.com/jdhp-sap/tino_cta#edge-rejection
    """

    try:
        mask = np.ones(img.shape, dtype=np.bool_)
        mask[1:-1, 1:-1] = 0
        res = float(np.nanmax(img[mask]))
    except:
        res = None

    return res

