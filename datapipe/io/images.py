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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import os

# EXCEPTIONS #################################################################

class FitsError(Exception):
    pass

class WrongHDUError(FitsError):
    """Exception raised when trying to access a wrong HDU in a FITS file.

    Attributes:
        file_path -- the FITS file concerned by the error
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
        file_path -- the FITS file concerned by the error
        hdu_index -- the HDU index concerned by the error
    """

    def __init__(self, file_path, hdu_index):
        super(NotAnImageError, self).__init__("HDU {} in file {} doesn't contain any image.".format(hdu_index, file_path))
        self.file_path = file_path
        self.hdu_index = hdu_index

class WrongDimensionError(FitsError):
    """
    Exception raised when trying to save a FITS with more than 3 dimensions
    or less than 2 dimensions.
    """

    def __init__(self):
        super(WrongDimensionError, self).__init__("The input image should be a 2D or a 3D numpy array.")

class WrongFitsFileStructure(FitsError):
    """Exception raised when trying to load a FITS file which doesn't contain a
    valid structure (for benchmark).

    Attributes:
        file_path -- the FITS file concerned by the error
    """

    def __init__(self, file_path):
        super(WrongFitsFileStructure, self).__init__("File {} doesn't contain a valid structure.".format(file_path))
        self.file_path = file_path


# LOAD BENCHMARK IMAGE #######################################################

def load_benchmark_images(input_file_path):
    """Return images contained in the given FITS file.

    Parameters
    ----------
    input_file_path : str
        The path of the FITS file to load

    Returns
    -------
    dict
        A dictionary containing the loaded images and their metadata

    Raises
    ------
    WrongFitsFileStructure
        If `input_file_path` doesn't contain a valid structure
    """

    hdu_list = fits.open(input_file_path)   # open the FITS file

    if (len(hdu_list) != 7) or (not hdu_list[0].is_image) or (not hdu_list[1].is_image) or (not hdu_list[2].is_image) or (not hdu_list[3].is_image) or (not hdu_list[4].is_image) or (not hdu_list[5].is_image) or (not hdu_list[6].is_image):
        hdu_list.close()
        raise WrongFitsFileStructure(input_file_path)

    hdu0, hdu1, hdu2, hdu3, hdu4, hdu6, hdu7 = hdu_list

    # IMAGES

    images_dict = {}

    images_dict["input_image"] = hdu0.data        # "hdu.data" is a Numpy Array
    images_dict["reference_image"] = hdu1.data    # "hdu.data" is a Numpy Array
    images_dict["adc_sum_image"] = hdu2.data      # "hdu.data" is a Numpy Array
    images_dict["pedestal_image"] = hdu3.data     # "hdu.data" is a Numpy Array
    images_dict["gains_image"] = hdu4.data        # "hdu.data" is a Numpy Array
    #images_dict["calibration_image"] = hdu5.data # "hdu.data" is a Numpy Array
    images_dict["pixels_position"] = hdu6.data    # "hdu.data" is a Numpy Array
    images_dict["pixels_mask"] = hdu7.data        # "hdu.data" is a Numpy Array

    # METADATA

    metadata_dict = {}

    metadata_dict['npe'] = float(images_dict["reference_image"].sum())       # np.sum() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...
    metadata_dict['min_npe'] = float(images_dict["reference_image"].min())   # np.min() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...
    metadata_dict['max_npe'] = float(images_dict["reference_image"].max())   # np.max() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...

    metadata_dict['tel_id'] = hdu0.header['tel_id']
    metadata_dict['event_id'] = hdu0.header['event_id']
    metadata_dict['simtel_path'] = hdu0.header['simtel']

    metadata_dict['num_tel_with_trigger'] = hdu0.header['tel_trig']

    metadata_dict['mc_energy'] = hdu0.header['energy']
    metadata_dict['mc_energy_unit'] = hdu0.header.comments['energy']

    metadata_dict['mc_azimuth'] = hdu0.header['mc_az']
    metadata_dict['mc_azimuth_unit'] = hdu0.header.comments['mc_az']

    metadata_dict['mc_altitude'] = hdu0.header['mc_alt']
    metadata_dict['mc_altitude_unit'] = hdu0.header.comments['mc_alt']

    metadata_dict['mc_core_x'] = hdu0.header['mc_corex']
    metadata_dict['mc_core_x_unit'] = hdu0.header.comments['mc_corex']

    metadata_dict['mc_core_y'] = hdu0.header['mc_corey']
    metadata_dict['mc_core_y_unit'] = hdu0.header.comments['mc_corey']

    metadata_dict['mc_height_first_interaction'] = hdu0.header['mc_hfi']
    metadata_dict['mc_height_first_interaction_unit'] = hdu0.header.comments['mc_hfi']

    metadata_dict['ev_count'] = hdu0.header['count']
    metadata_dict['run_id'] = hdu0.header['run_id']
    metadata_dict['num_tel_with_data'] = hdu0.header['tel_data']

    metadata_dict['optical_foclen'] = hdu0.header['foclen']
    metadata_dict['optical_foclen_unit'] = hdu0.header.comments['foclen']

    metadata_dict['tel_pos_x'] = hdu0.header['tel_posx']
    metadata_dict['tel_pos_x_unit'] = hdu0.header.comments['tel_posx']

    metadata_dict['tel_pos_y'] = hdu0.header['tel_posy']
    metadata_dict['tel_pos_y_unit'] = hdu0.header.comments['tel_posy']

    metadata_dict['tel_pos_z'] = hdu0.header['tel_posz']
    metadata_dict['tel_pos_z_unit'] = hdu0.header.comments['tel_posz']

    # TODO: Astropy fails to store the following data in FITS files
    #metadata_dict['uid'] = hdu0.header.comments['uid']
    #metadata_dict['date_time'] = hdu0.header.comments['datetime']
    #metadata_dict['version'] = hdu0.header.comments['version']
    #metadata_dict['argv'] = hdu0.header.comments['argv']
    #metadata_dict['python_version'] = hdu0.header.comments['python']
    #metadata_dict['system'] = hdu0.header.comments['system']

    hdu_list.close()

    return images_dict, metadata_dict


# SAVE BENCHMARK IMAGE #######################################################

def save_benchmark_images(img,
                          pe_img,
                          adc_sums_img,
                          pedestal_img,
                          gains_img,
                          #calibration_img,
                          pixel_pos,
                          pixel_mask,
                          metadata,
                          output_file_path):
    """
    Write a FITS file containing pe_img, output_file_path and metadata.

    Parameters
    ----------
    img: ndarray
        The "input image" to save (it should be a 2D Numpy array).
    pe_img: ndarray
        The "reference image" to save (it should be a 2D Numpy array).
    output_file_path: str
        The path of the output FITS file.
    metadata: tuple
        A dictionary containing all metadata to write in the FITS file.
    """

    if img.ndim != 2:
        raise Exception("The input image should be a 2D numpy array.")

    if pe_img.ndim != 2:
        raise Exception("The input image should be a 2D numpy array.")

    if adc_sums_img.ndim != 3:
        raise Exception("The input image should be a 3D numpy array.")

    if pedestal_img.ndim != 3:
        raise Exception("The input image should be a 3D numpy array.")

    if gains_img.ndim != 3:
        raise Exception("The input image should be a 3D numpy array.")

    #if calibration_img.ndim != 3:
    #    raise Exception("The input image should be a 3D numpy array.")

    if pixel_pos.ndim != 3:
        raise Exception("The input image should be a 3D numpy array.")

    if pixel_mask.ndim != 2:
        raise Exception("The input image should be a 2D numpy array.")

    # http://docs.astropy.org/en/stable/io/fits/appendix/faq.html#how-do-i-create-a-multi-extension-fits-file-from-scratch
    # http://docs.astropy.org/en/stable/generated/examples/io/create-mef.html#sphx-glr-generated-examples-io-create-mef-py
    hdu0 = fits.PrimaryHDU(img)
    hdu1 = fits.ImageHDU(pe_img)
    hdu2 = fits.ImageHDU(adc_sums_img)
    hdu3 = fits.ImageHDU(pedestal_img)
    hdu4 = fits.ImageHDU(gains_img)
    #hdu5 = fits.ImageHDU(calibration_img)
    hdu6 = fits.ImageHDU(pixel_pos)
    hdu7 = fits.ImageHDU(pixel_mask)

    hdu0.header["desc"] = "calibrated image"
    hdu1.header["desc"] = "pe image"
    hdu2.header["desc"] = "adc sum images"
    hdu3.header["desc"] = "pedestal images"
    hdu4.header["desc"] = "gains images"
    #hdu5.header["desc"] = "calibration images"
    hdu6.header["desc"] = "pixels position"
    hdu7.header["desc"] = "pixels mask"

    for key, val in metadata.items():
        if type(val) is tuple :
            hdu0.header[key] = val[0]
            hdu0.header.comments[key] = val[1]
        else:
            hdu0.header[key] = val

    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    hdu_list = fits.HDUList([hdu0, hdu1, hdu2, hdu3, hdu4, hdu6, hdu7])

    hdu_list.writeto(output_file_path)


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

COLOR_MAP = cm.gnuplot2

def mpl_save(img, output_file_path, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=24)

    #im = ax.imshow(img,
    #               origin='lower',
    #               interpolation='nearest',
    #               vmin=min(img.min(), 0),
    #               cmap=COLOR_MAP)

    # Manage NaN values (see http://stackoverflow.com/questions/2578752/how-can-i-plot-nan-values-as-a-special-color-with-imshow-in-matplotlib and http://stackoverflow.com/questions/38800532/plot-color-nan-values)
    masked = np.ma.masked_where(np.isnan(img), img)

    cmap = COLOR_MAP
    cmap.set_bad('black')
    im = ax.imshow(masked,
                   origin='lower',
                   interpolation='nearest',
                   cmap=cmap)

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

    #im = ax.imshow(img,
    #               origin='lower',
    #               interpolation='nearest',
    #               vmin=min(img.min(), 0),
    #               cmap=COLOR_MAP)

    # Manage NaN values (see http://stackoverflow.com/questions/2578752/how-can-i-plot-nan-values-as-a-special-color-with-imshow-in-matplotlib and http://stackoverflow.com/questions/38800532/plot-color-nan-values)
    masked = np.ma.masked_where(np.isnan(img), img)

    cmap = COLOR_MAP
    cmap.set_bad('black')
    im = ax.imshow(masked,
                   origin='lower',
                   interpolation='nearest',
                   cmap=cmap)

    plt.colorbar(im) # draw the colorbar

    plt.show()


def plot_hist(img, num_bins=50, logx=False, logy=False, x_max=None, title=""):
    """
    """

    # Flatten + remove NaN values
    flat_img = img[np.isfinite(img)]

    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title)

    if logx:
        # Setup the logarithmic scale on the X axis
        vmin = np.log10(flat_img.min())
        vmax = np.log10(flat_img.max())
        bins = np.logspace(vmin, vmax, num_bins) # Make a range from 10**vmin to 10**vmax
    else:
        bins = num_bins

    if x_max is not None:
        ax.set_xlim(xmax=x_max)

    res_tuple = ax.hist(flat_img,
                        bins=bins,
                        log=logy,               # Set log scale on the Y axis
                        histtype='bar',
                        alpha=1)

    if logx:
        ax.set_xscale("log")               # Activate log scale on X axis

    plt.show()


###############################################################################


def _plot_list(img_list, title_list, main_title=None):
    fig, ax_tuple = plt.subplots(nrows=1, ncols=len(img_list), figsize=(12, 4))

    for img, title, ax in zip(img_list, title_list, ax_tuple):
        ax.set_title(title)

        #im = ax.imshow(img,
        #               origin='lower',
        #               interpolation='nearest',
        #               vmin=min(img.min(), 0),
        #               cmap=COLOR_MAP)

        # Manage NaN values (see http://stackoverflow.com/questions/2578752/how-can-i-plot-nan-values-as-a-special-color-with-imshow-in-matplotlib and http://stackoverflow.com/questions/38800532/plot-color-nan-values)
        masked = np.ma.masked_where(np.isnan(img), img)

        cmap = cm.gnuplot2
        cmap.set_bad('black')
        im = ax.imshow(masked,
                       origin='lower',
                       interpolation='nearest',
                       cmap=cmap)

        plt.colorbar(im, ax=ax) # draw the colorbar

    if main_title is not None:
        fig.suptitle(main_title, fontsize=18)
        plt.subplots_adjust(top=0.85)


def plot_list(img_list, title_list, metadata_dict=None):
    """
    img should be a list of 2D numpy array.
    """

    # Main title
    if metadata_dict is not None:
        main_title = "{} (Tel. {}, Ev. {}) {:.2E}{}".format(os.path.basename(metadata_dict['simtel_path']),
                                                            metadata_dict['tel_id'],
                                                            metadata_dict['event_id'],
                                                            metadata_dict['mc_energy'],
                                                            metadata_dict['mc_energy_unit'])

    _plot_list(img_list, title_list, main_title)
    plt.show()


def mpl_save_list(img_list, output_file_path, title_list, metadata_dict=None):
    """
    img should be a list of 2D numpy array.
    """
    # Main title
    if metadata_dict is not None:
        main_title = "{} (Tel. {}, Ev. {}) {:.2E}{}".format(os.path.basename(metadata_dict['simtel_path']),
                                                            metadata_dict['tel_id'],
                                                            metadata_dict['event_id'],
                                                            metadata_dict['mc_energy'],
                                                            metadata_dict['mc_energy_unit'])

    _plot_list(img_list, title_list, main_title)
    plt.savefig(output_file_path, bbox_inches='tight')
    plt.close('all')


# DEBUG #######################################################################

def export_image_as_plain_text(image, output_file_path):
    fd = open(output_file_path, 'w')
    for x in image:
        for y in x:
            print("{:5.2f}".format(y), end=" ", file=fd)
        print("", file=fd)
    fd.close()
