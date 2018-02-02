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
from ctapipe.image.hillas import hillas_parameters_3
from ctapipe.image.hillas import hillas_parameters_4

from ctapipe.instrument import CameraGeometry

import copy

"""
Warning: so far, this module only works with "rectangular 2D images", but it
handle "missing pixels" (i.e. NaN values).
"""

def get_hillas_parameters(geom: CameraGeometry, image, implementation=4):
    r"""Return Hillas parameters [hillas]_ of the given ``image``.

    See https://github.com/cta-observatory/ctapipe/blob/master/ctapipe/image/hillas.py#L83
    for more information.

    Parameters
    ----------
    geom : CameraGeomatry
        The geometry of the image to parametrize

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

    if implementation == 1:
        params = hillas_parameters_1(geom, image)
    elif implementation == 2:
        params = hillas_parameters_2(geom, image)
    elif implementation == 3:
        params = hillas_parameters_3(geom, image)
    elif implementation == 4:
        params = hillas_parameters_4(geom, image)
    else:
        raise ValueError("Wrong Hillas implementation ID.")

    return params
