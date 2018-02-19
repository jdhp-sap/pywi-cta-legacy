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

__all__ = ['get_geom1d',
           'image_2d_to_1d',
           'image_1d_to_2d']

import ctapipe.image.geometry_converter as geomconv
from ctapipe.instrument import camera

import numpy as np
import sys

"""
Convert the 2D array image format used by the wavelet image cleaning to the
1D array image format used by ctapipe.
"""

def get_geom1d(cam_id):
    """Return the `cam_id` geometry for ctapipe.

    Use `camera.CameraGeometry.get_known_camera_names()` to get the list of
    available cameras.

    Parameters
    ----------
    cam_id: str
        The instrument name (required to guess the image geometry).

    Returns
    -------
    geom1d: CameraGeometry
        The `cam_id` camera geometry for ctapipe **1D images**.
    """

    # Use a cache to speedup geom access (~1 micro sec instead of ~70 micro sec)
    geometry_converter_module = sys.modules[__name__]
    var_name = "_geom1d_" + cam_id

    if hasattr(geometry_converter_module, var_name):

        geom1d = getattr(geometry_converter_module, var_name)

    else:

        camera_names = camera.CameraGeometry.get_known_camera_names()

        if cam_id not in camera_names:
            error_str = "Unknown camera name {}. Should be one of: {}.".format(cam_id, ", ".join(camera_names))
            raise ValueError(error_str)

        geom1d = camera.CameraGeometry.from_name(cam_id)
        setattr(geometry_converter_module, var_name, geom1d)

    return geom1d

def get_geom2d(cam_id):
    """TODO!!!!!!!!!!!!!

    TODO: this implementation is a temporary hack...
    ctapipe.image.geometry_converter should be updated to clean this
    function...
    """
    geom1d = get_geom1d(cam_id)  # TODO: should be avoided...

    if cam_id in ("DigiCam", "NectarCam", "FlashCam", "LSTCam"):
        # TODO: dirty hack !!!!!!!!!!!
        rotation = 0
        geom2d, image2d = geomconv.convert_geometry_hex1d_to_rect2d(geom1d,
                                                                    np.zeros(geom1d.pix_x.shape),
                                                                    geom1d.cam_id + str(rotation),
                                                                    add_rot=rotation) # TODO
    elif cam_id == "ASTRICam":
        num_pixels_x = 7*8
        num_pixels_y = 7*8

        geom1d = get_geom1d(cam_id)

        range_x = (geom1d.pix_x.value.min(), geom1d.pix_x.value.max())
        range_y = (geom1d.pix_y.value.min(), geom1d.pix_y.value.max())

        geom2d = camera.CameraGeometry.make_rectangular(num_pixels_x,
                                                        num_pixels_y,
                                                        range_x,
                                                        range_y)
        geom2d.cam_id = "ASTRICam2D"
        #shape_2d = (num_pixels_x, num_pixels_y)
        #geom2d.pix_x = geom2d.pix_x.reshape(shape_2d)
        #geom2d.pix_y = geom2d.pix_y.reshape(shape_2d)
        ##geom2d.mask = geom2d.mask.reshape(shape_2d)
        #geom2d.pix_area = geom2d.pix_area.reshape(shape_2d)
        raise NotImplementedError()
    elif cam_id == "CHEC":
        num_pixels_x = 6*8
        num_pixels_y = 6*8

        geom1d = get_geom1d(cam_id)

        range_x = (geom1d.pix_x.value.min(), geom1d.pix_x.value.max())
        range_y = (geom1d.pix_y.value.min(), geom1d.pix_y.value.max())

        geom2d = camera.CameraGeometry.make_rectangular(num_pixels_x,
                                                        num_pixels_y,
                                                        range_x,
                                                        range_y)
        geom2d.cam_id = "CHEC2D"
        raise NotImplementedError()
    else:
        raise ValueError("1D to 2D image converter: unknown camera {}.".format(cam_id))

    return geom2d

def image_2d_to_1d(image2d, cam_id):
    """Convert a wavelet compatible 2D image to a ctapipe compliant 1D image.

    Convert the 2D array image format used by the wavelet image cleaning to the
    1D array image format used by ctapipe.

    Parameters
    ----------
    image2d: 2D ndarray
        The 2D image to convert.
    cam_id: str
        The instrument name (required to guess the image geometry).

    Returns
    -------
    1D ndarray
        The converted image in its 1D version compliant with ctapipe.
    """

    geom1d = get_geom1d(cam_id)  # TODO: should be avoided...

    if cam_id in ("DigiCam", "NectarCam", "FlashCam", "LSTCam"):
        rotation = 0  # TODO: should be avoided...
        _, image1d = geomconv.convert_geometry_rect2d_back_to_hexe1d(geom1d,
                                                                     image2d,
                                                                     cam_id + str(rotation),
                                                                     add_rot=rotation) # TODO
    elif cam_id == "ASTRICam":
        image1d = geomconv.array_2d_to_astri(image2d)
    elif cam_id == "CHEC":
        image1d = geomconv.array_2d_to_chec(image2d)
    else:
        raise ValueError("2D to 1D image converter: unknown camera {}.".format(cam_id))

    return image1d

def image_1d_to_2d(image1d, cam_id):
    """Convert a ctapipe compliant 1D image to a wavelet compatible 2D image.

    Convert the 1D array image format used by ctapipe to the 2D array image
    format used by the wavelet image cleaning.

    Parameters
    ----------
    image1d: 1D ndarray
        The 1D image to convert.
    cam_id: str
        The instrument name (required to guess the image geometry).

    Returns
    -------
    2D ndarray
        The converted image in its 2D version compliant with wavelet packages.
    """

    geom1d = get_geom1d(cam_id)  # TODO: should be avoided...

    if cam_id in ("DigiCam", "NectarCam", "FlashCam", "LSTCam"):
        rotation = 0  # TODO: should be avoided...
        geom2d, image2d = geomconv.convert_geometry_hex1d_to_rect2d(geom1d,
                                                                    image1d,
                                                                    cam_id + str(rotation),
                                                                    add_rot=rotation) # TODO
    elif cam_id == "ASTRICam":
        image2d = geomconv.astri_to_2d_array(image1d)
    elif cam_id == "CHEC":
        image2d = geomconv.chec_to_2d_array(image1d)
    else:
        raise ValueError("1D to 2D image converter: unknown camera {}.".format(cam_id))

    return image2d
