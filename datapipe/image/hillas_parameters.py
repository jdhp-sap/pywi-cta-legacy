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

__all__ = ['get_hillas_parameters']

from ctapipe.image.hillas import hillas_parameters_1
from ctapipe.image.hillas import hillas_parameters_2

import astropy.units as u

import numpy as np

"""
Warning: so far, this module only works with "rectangular 2D images".
"""

def get_hillas_parameters(image, implementation=2):
    r"""Return Hillas parameters [hillas]_ of the given ``image``.

    See https://github.com/cta-observatory/ctapipe/blob/master/ctapipe/image/hillas.py#L83
    for more information.

    Parameters
    ----------
    image : Numpy array
        The image to parametrize

    implementation : integer
        Tell which ctapipe's implementation to use (1 or 2).

    Returns
    -------
    namedtuple
        Hillas parameters for the given ``image``

    References
    ----------
    .. [hillas] Appendix of the Whipple Crab paper Weekes et al. (1998)
       http://adsabs.harvard.edu/abs/1989ApJ...342..379W
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    image = image.astype('float64', copy=True)

    x = np.arange(0, np.shape(image)[0], 1)
    y = np.arange(0, np.shape(image)[1], 1)
    xx, yy = np.meshgrid(x, y)

    if implementation == 1:
        params = hillas_parameters_1(xx.flatten() * u.meter, yy.flatten() * u.meter, image.flatten())
    else:
        params = hillas_parameters_2(xx.flatten() * u.meter, yy.flatten() * u.meter, image.flatten())

    return params


