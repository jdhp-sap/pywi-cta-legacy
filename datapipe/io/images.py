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


# EXCEPTIONS #################################################################

class FitsError(Exception):
    pass

class WrongHDUError(FitsError):
    """Exception raised when trying to access a wrong HDU in a FITS file.

    Attributes:
        input_file_path -- the FITS file concerned by the error
        hdu_index -- the HDU index concerned by the error
    """

    def __init__(self, file_path, hdu_index):
        super(WrongHDUError, self).__init__("File {} doesn't have data in HDU {}.".format(file_path, hdu_index))
        self.file_path = file_path
        self.hdu_index = hdu_index

class NotAnImageError(FitsError):
    """Exception raised when trying to load a FITS file which doesn't contain a
    valid image in the given HDU.

    Attributes:
        input_file_path -- the FITS file concerned by the error
        hdu_index -- the HDU index concerned by the error
    """

    def __init__(self, input_file_path, hdu_index):
        super(NotAnImageError, self).__init__("HDU {} in file {} doesn't contain any image.".format(self.hdu_index, self.file_path))
        self.file_path = file_path
        self.hdu_index = hdu_index

class WrongDimensionError(FitsError):
    """
    Exception raised when trying to save a FITS with more than 3 dimensions
    or less than 2 dimensions.
    """

    def __init__(self):
        super(WrongDimensionError, self).__init__("The input image should be a 2D or a 3D numpy array.")


# LOAD AND SAVE FITS FILES ###################################################

def load(input_file_path, hdu_index):
    """Return the image array contained in the given HDU of the given FITS file.

    Parameters
    ----------
    input_file_path : str
        The path of the FITS file to load
    hdu_index : int
        The HDU to load within the FITS file (one FITS file can contain several
        images stored in different HDU)

    Returns
    -------
    ndarray
        The loaded image

    Raises
    ------
    WrongHDUError
        If `input_file_path` doesn't contain the HDU `hdu_index`
    NotAnImageError
        If `input_file_path` doesn't contain a valid image in the HDU
        `hdu_index`
    """
    
    hdu_list = fits.open(input_file_path)   # open the FITS file

    if not (0 <= hdu_index < len(hdu_list)):
        hdu_list.close()
        raise WrongHDUError(input_file_path, hdu_index)

    hdu = hdu_list[hdu_index]

    if not hdu.is_image:
        hdu_list.close()
        raise NotAnImageError(input_file_path, hdu_index)

    image_array = hdu.data    # "hdu.data" is a Numpy Array

    hdu_list.close()

    return image_array


def save(img, output_file_path):
    """Save the `img` image array to the `output_file_path` FITS file.

    Parameters
    ----------
    img : ndarray
        The image to save (should be a 2D or a 3D numpy array)
    output_file_path : str
        The path of the FITS file where to save the `img`

    Raises
    ------
    WrongDimensionError
        If `img` has more than 3 dimensions or less than 2 dimensions.
    """

    if img.ndim not in (2, 3):
        raise WrongDimensionError()

    hdu = fits.PrimaryHDU(img)

    hdu.writeto(output_file_path, clobber=True)  # clobber=True: overwrite the file if it already exists


# MATPLOTLIB ##################################################################

COLOR_MAP = "gnuplot2" # "gray"

def mpl_save(img, output_file_path, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=24)

    im = ax.imshow(img,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min(img.min(), 0),
                   cmap=COLOR_MAP)

    plt.colorbar(im) # draw the colorbar

    plt.savefig(output_file_path, bbox_inches='tight')
    plt.close('all')


def plot(img, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title)

    im = ax.imshow(img,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min(img.min(), 0),
                   cmap=COLOR_MAP)

    plt.colorbar(im) # draw the colorbar

    plt.show()


def mpl_save_list(img_list, output_file_path, title_list):
    """
    img should be a list of 2D numpy array.
    """
    fig, ax_tuple = plt.subplots(nrows=1, ncols=len(img_list), figsize=(12, 4))

    for img, title, ax in zip(img_list, title_list, ax_tuple):
        ax.set_title(title, fontsize=18)

        im = ax.imshow(img,
                       origin='lower',
                       interpolation='nearest',
                       vmin=min(img.min(), 0),
                       cmap=COLOR_MAP)

        plt.colorbar(im, ax=ax) # draw the colorbar

    plt.savefig(output_file_path, bbox_inches='tight')
    plt.close('all')


def plot_list(img_list, title_list):
    """
    img should be a list of 2D numpy array.
    """
    fig, ax_tuple = plt.subplots(nrows=1, ncols=len(img_list), figsize=(12, 4))

    for img, title, ax in zip(img_list, title_list, ax_tuple):
        ax.set_title(title)

        im = ax.imshow(img,
                       origin='lower',
                       interpolation='nearest',
                       vmin=min(img.min(), 0),
                       cmap=COLOR_MAP)

        plt.colorbar(im, ax=ax) # draw the colorbar

    plt.show()

