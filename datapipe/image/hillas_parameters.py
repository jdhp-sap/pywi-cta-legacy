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
import copy

import numpy as np

"""
Warning: so far, this module only works with "rectangular 2D images", but it
handle "missing pixels" (i.e. NaN values).
"""

def get_hillas_parameters(image, implementation=2, pixels_position=None):
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

    # Copy image to prevent tricky bugs
    image = image.copy()

    # Flatten image and remove NaN values
    flat_img = image[np.isfinite(image)]

    if pixels_position is not None:
        # Copy pixel_position to prevent tricky bugs
        #pixels_position = (np.copy(pixels_position[0]), np.copy(pixels_position[1]))
        pixels_position = copy.deepcopy(pixels_position)

        # Flatten pixels_position and remove NaN values
        xx = pixels_position[0][np.isfinite(pixels_position[0])]
        yy = pixels_position[1][np.isfinite(pixels_position[1])]
    else:
        x = np.arange(0, np.shape(image)[1])
        y = np.arange(0, np.shape(image)[0])
        xx, yy = np.meshgrid(x, y)

        # Flatten pixels_position and remove pixels that are NaN in `image`
        xx = xx[np.isfinite(image)].flatten()
        yy = yy[np.isfinite(image)].flatten()

    if implementation == 1:
        params = hillas_parameters_1(xx * u.meter, yy * u.meter, flat_img)
    else:
        params = hillas_parameters_2(xx * u.meter, yy * u.meter, flat_img)

    return params
