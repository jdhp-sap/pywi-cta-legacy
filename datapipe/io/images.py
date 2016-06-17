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
import matplotlib.pyplot as plt
from matplotlib import cm

def load(input_file_path, hdu_index):
    """
    Return the image array contained in the first HDU of the given FITS file.
    """
    
    hdu_list = fits.open(input_file_path)   # open the FITS file

    if not (0 <= hdu_index < len(hdu_list)):
        raise Exception("Wrong HDU index.")

    hdu = hdu_list[hdu_index]

    if not hdu.is_image:
        raise Exception("HDU{} doesn't contain any image.".format(hdu_index))

    image_array = hdu.data    # "hdu.data" is a Numpy Array

    hdu_list.close()

    return image_array


def save(img, output_file_path, min_val=None, max_val=None):
    """
    img is the image and it should be a 2D or a 3D numpy array with values.
    """

    if img.ndim not in (2, 3):
        raise Exception("The input image should be a 2D or a 3D numpy array.")

    hdu = fits.PrimaryHDU(img)

    hdu.writeto(output_file_path, clobber=True)  # clobber=True: overwrite the file if it already exists


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

