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

__all__ = ['load',
           'save',
           'mpl_save',
           'plot']

from astropy.io import fits

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import PIL.Image as pil_img     # PIL.Image is a module not a class...

def load(input_file_path):
    """
    Return the image array contained in the first HDU of the given FITS file.
    """
    
    file_extension = os.path.splitext(input_file_path)[1].lower()

    if file_extension == ".fits":

        hdu_list = fits.open(input_file_path)   # open the FITS file

        if len(hdu_list) != 1:
            raise Exception("The FITS file should contain only one HDU.")

        image_array = hdu_list[0].data    # "hdu.data" is a Numpy Array

        hdu_list.close()

    elif file_extension in (".png", ".jpg", ".jpeg"):

        # Open the image and convert it to grayscale
        image_array = np.array(pil_img.open(input_file_path).convert('L'))

    else:

        raise Exception("Unrecognized input file format.")

    return image_array


def save(img, output_file_path, min_val=None, max_val=None):
    """
    img is the image and it should be a 2D or a 3D numpy array with values.
    """

    file_extension = os.path.splitext(output_file_path)[1].lower()

    if file_extension == ".fits":

        if img.ndim not in (2, 3):
            raise Exception("The input image should be a 2D or a 3D numpy array.")

        hdu = fits.PrimaryHDU(img)

        if os.path.isfile(output_file_path):
            os.remove(output_file_path)

        hdu.writeto(output_file_path)

    elif file_extension in (".png", ".jpg", ".jpeg"):

        if img.ndim != 2:
            raise Exception("The input image should be a 2D numpy array.")

        # Normalize values ################
        # (FITS pixels value are unbounded but PNG pixels value are in range [0,255])
        if min_val == None:
            min_val = img.min()
        if max_val == None:
            max_val = img.max()

        img = img.astype(np.float32)
        img -= min_val
        img /= max_val
        img *= 255
        img = img.astype(np.uint8)

        # Save
        mode = "L"                           # "L" = grayscale mode
        pil_image = pil_img.new(mode, img.shape)

        # WARNING: nested list and 2D numpy arrays are silently rejected!!!
        #          data *must* be a list or a 1D numpy array!
        pil_image.putdata(img.flatten())
        pil_image.save(output_file_path)

    else:

        raise Exception("Unrecognized output file format.")



# MATPLOTLIB ##################################################################

def mpl_save(img, output_file_path, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=24)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.savefig(output_file_path, bbox_inches='tight')
    plt.close('all')


def plot(img, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.show()

