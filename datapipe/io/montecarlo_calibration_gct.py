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

"""

__all__ = ['apply_mc_calibration']

import numpy as np
import pyhessio

#def get_mc_calibration_data(tel_id):
#    """
#    Get the calibration coefficients from the MC data file to the data.
#    This is ahack (until we have a real data structure for the calibrated
#    data), it should move into `ctapipe.io.hessio_event_source`.
#
#    Parameters
#    ----------
#    tel_id : int
#        The ID of the telescope to process. 
#
#    Returns
#    -------
#    tuple of Numpy array
#        A tuble containing 2 elements: ``pedestal`` a 2D arrays of the pedestal
#        (one dimension for each channel) and ``gain`` a 2D arrays of the PE/DC
#        ratios (one dimension for each channel).
#    """
#    pedestal = pyhessio.get_pedestal(tel_id)
#    gains = pyhessio.get_calibration(tel_id)
#
#    return pedestal, gains


def apply_mc_calibration(adcs, peds, gains):
    """
    Apply basic calibration.

    Parameters
    ----------
    adc : Numpy array
        The uncalibrated ADC signal (one dimension per channel). 
    peds : Numpy array
        The pedestal (one dimension per channel). 
    gains : Numpy array
        The gains (one dimension per channel). 
    """

    calibrated_image = (adcs[0] - peds[0]) * gains[0]

    return calibrated_image

