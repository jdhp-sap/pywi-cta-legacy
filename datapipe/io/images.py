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
           'plot',
           'image_files_in_dir',
           'image_files_in_paths',
           'image_generator']

import math

import collections

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Ellipse

import os

from astropy.io import fits
import astropy.units as u

import ctapipe
from ctapipe.io.hessio import hessio_event_source
from ctapipe.instrument import CameraGeometry
from ctapipe.calib import CameraCalibrator
import ctapipe.visualization

from datapipe.image.hillas_parameters import get_hillas_parameters
from datapipe.io import geometry_converter

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
        super().__init__("File {} doesn't have data in HDU {}.".format(file_path, hdu_index))
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
        super().__init__("HDU {} in file {} doesn't contain any image.".format(hdu_index, file_path))
        self.file_path = file_path
        self.hdu_index = hdu_index

class WrongDimensionError(FitsError):
    """ Exception raised when trying to save a FITS with more than 3 dimensions
    or less than 2 dimensions.
    """

    def __init__(self):
        super().__init__("The input image should be a 2D or a 3D numpy array.")

class WrongFitsFileStructure(FitsError):
    """Exception raised when trying to load a FITS file which doesn't contain a
    valid structure (for benchmark).

    Attributes:
        file_path -- the FITS file concerned by the error
    """

    def __init__(self, file_path):
        super().__init__("File {} doesn't contain a valid structure.".format(file_path))
        self.file_path = file_path


# DIRECTORY PARSER ############################################################

def image_files_in_dir(directory_path, max_num_files=None):
    """ Return the list of all FITS files and Simtel files in `directory_path`.
    """

    FILE_EXT = (".simtel", ".simtel.gz", ".fits", ".fit")
    directory_path = os.path.expanduser(directory_path)

    files_counter = 0

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(FILE_EXT):
            files_counter += 1
            if (max_num_files is not None) and (files_counter > max_num_files):
                break
            else:
                yield file_path


def image_files_in_paths(path_list, max_num_files=None):
    """Return an iterable sequence all FITS files path and Simtel files path in `path_list`.

    `path_list` can contain files and directories.
    """

    files_counter = 0

    for path in path_list:
        if os.path.isdir(path):
            # If path is a directory
            for file_path in image_files_in_dir(path):
                files_counter += 1
                if (max_num_files is not None) and (files_counter > max_num_files):
                    break
                else:
                    yield file_path
        elif os.path.isfile(path):
            # If path is a regular file
            files_counter += 1
            if (max_num_files is not None) and (files_counter > max_num_files):
                break
            else:
                yield path
        else:
            raise Exception("Wrong item:", path)


# LOAD IMAGES ################################################################

Image1D = collections.namedtuple('Image1D', ('input_image',
                                             'reference_image',
                                             'adc_sum_image',
                                             'pedestal_image',
                                             'gains_image',
                                             'pixels_position',
                                             'meta'))

Image2D = collections.namedtuple('Image2D', ('input_image',
                                             'reference_image',
                                             'adc_sum_image',
                                             'pedestal_image',
                                             'gains_image',
                                             'pixels_position',
                                             'pixels_mask',
                                             'meta'))

def image_generator(path_list,
                    max_num_images=None,
                    tel_filter_list=None,
                    ev_filter_list=None,
                    cam_filter_list=None,
                    **kwargs):
    """Return an iterable sequence all calibrated images in `path_list`.

    Parameters
    ----------
    path_list
        The path of files containing the images to extract. It can contain
        FITS/Simtel files and directories.
    max_num_images
        The maximum number of images to iterate.
    tel_filter_list
        Only iterate images from telescopes defined in this list.
    ev_filter_list
        Only iterate images from events defined in this list.
    cam_filter_list
        Only iterate images from cameras defined in this list.
    """

    images_counter = 0

    for file_path in image_files_in_paths(path_list):
        if file_path.lower().endswith((".simtel", ".simtel.gz")):
            # SIMTEL FILES
            for image in simtel_images_generator(file_path, tel_filter_list, ev_filter_list, **kwargs):
                if (max_num_images is not None) and (images_counter >= max_num_images):
                    break
                else:
                    if (tel_filter_list is None) or (image.meta['tel_id'] in tel_filter_list):
                        if (ev_filter_list is None) or (image.meta['event_id'] in ev_filter_list):
                            if (cam_filter_list is None) or (image.meta['cam_id'] in cam_filter_list):
                                images_counter += 1
                                yield image
        elif file_path.lower().endswith((".fits", ".fit")):
            # FITS FILES
            if (max_num_images is not None) and (images_counter >= max_num_images):
                break
            else:
                image_dict, fits_metadata_dict = load_benchmark_images(file_path)   # TODO: named tuple
                if (tel_filter_list is None) or (fits_metadata_dict['tel_id'] in tel_filter_list):
                    if (ev_filter_list is None) or (fits_metadata_dict['event_id'] in ev_filter_list):
                        if (cam_filter_list is None) or (fits_metadata_dict['cam_id'] in cam_filter_list):
                            images_counter += 1

                            yield Image2D(**image_dict, meta=fits_metadata_dict)
        else:
            raise Exception("Wrong item:", file_path)


# LOAD SIMTEL IMAGE ##########################################################

def quantity_to_tuple(quantity, unit_str):
    """Splits a quantity into a tuple of (value,unit) where unit is FITS compliant.

    Useful to write FITS header keywords with units in a comment.

    Parameters
    ----------
    quantity : astropy quantity
        The Astropy quantity to split.
    unit_str: str
        Unit string representation readable by astropy.units (e.g. 'm', 'TeV', ...)

    Returns
    -------
    tuple
        A tuple containing the value and the quantity.
    """
    return quantity.to(unit_str).value, quantity.to(unit_str).unit.to_string(format='FITS')


def simtel_event_to_images(event, tel_id, ctapipe_format=False):
    """
    TODO
    """

    SINGLE_CHANNEL_CAMERAS = ("CHEC", "DigiCam", "FlashCam")
    TWO_CHANNELS_CAMERAS = ("ASTRICam", "NectarCam", "LSTCam")

    # GUESS THE IMAGE GEOMETRY ################################

    x, y = event.inst.pixel_pos[tel_id]
    foclen = event.inst.optical_foclen[tel_id]
    geom1d = CameraGeometry.guess(x, y, foclen)

    # GET IMAGES ##############################################

    mc_pe = event.mc.tel[tel_id].photo_electron_image
    mc_pedestal = event.mc.tel[tel_id].pedestal                     # [N channels]
    mc_gain = event.mc.tel[tel_id].dc_to_pe                         # [N channels]

    r0_adc_sums = event.r0.tel[tel_id].adc_sums                     # [N channels]
    r0_adc_samples = event.r0.tel[tel_id].adc_samples               # [N channels]

    r1_pe_samples = event.r1.tel[tel_id].pe_samples                 # [N channels]

    dl0_pe_samples = event.dl0.tel[tel_id].pe_samples               # [N channels]

    dl1_cleaned_samples = event.dl1.tel[tel_id].cleaned             # [N channels]
    dl1_extracted_samples = event.dl1.tel[tel_id].extracted_samples # [N channels]
    dl1_image = event.dl1.tel[tel_id].image                         # [N channels]
    dl1_peakpos = event.dl1.tel[tel_id].peakpos                     # [N channels]

    # ALIAS #

    pe_image = mc_pe
    pedestal = mc_pedestal
    gain = mc_gain

    uncalibrated_image = r0_adc_sums
    uncalibrated_samples = r0_adc_samples

    calibrated_image = dl1_image.copy()

    pixel_pos = event.inst.pixel_pos[tel_id]

    cam_id = geom1d.cam_id

    # MIX CHANNELS FOR DOUBLE CHANNEL CAMERAS #################

    if cam_id == "ASTRICam":
        ASTRI_CAM_CHANNEL_THRESHOLD = 14         # cf. "calib_find_channel_selection_threshold" notebook
        calibrated_image[1, calibrated_image[0,:] <= ASTRI_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image[0, calibrated_image[0,:] >  ASTRI_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image = calibrated_image.sum(axis=0)
    elif cam_id == "NectarCam":
        NECTAR_CAM_CHANNEL_THRESHOLD = 190       # cf. "calib_find_channel_selection_threshold" notebook
        calibrated_image[1, calibrated_image[0,:] <= NECTAR_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image[0, calibrated_image[0,:] >  NECTAR_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image = calibrated_image.sum(axis=0)
    elif cam_id == "LSTCam":
        LST_CAM_CHANNEL_THRESHOLD = 100          # cf. "calib_find_channel_selection_threshold" notebook
        calibrated_image[1, calibrated_image[0,:] <= LST_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image[0, calibrated_image[0,:] >  LST_CAM_CHANNEL_THRESHOLD] = 0
        calibrated_image = calibrated_image.sum(axis=0)
    elif cam_id in SINGLE_CHANNEL_CAMERAS :
        calibrated_image = calibrated_image[0]
    else:
        raise ValueError("Unknown camera: {}".format(cam_id))

    # METADATA ###############################################

    metadata = {'cam_id': cam_id}

    ##########################################################

    if ctapipe_format:

        return Image1D(input_image=calibrated_image,
                       reference_image=pe_image,
                       adc_sum_image=uncalibrated_image,
                       pedestal_image=pedestal,
                       gains_image=gain,
                       pixels_position=pixel_pos,
                       meta=metadata)

    else:

        # CONVERTING GEOMETRY (1D TO 2D) ##########################

        if cam_id in SINGLE_CHANNEL_CAMERAS:

            pe_image_2d = geometry_converter.image_1d_to_2d(pe_image, cam_id=cam_id)
            calibrated_image_2d = geometry_converter.image_1d_to_2d(calibrated_image, cam_id=cam_id)

            uncalibrated_image_2d = geometry_converter.image_1d_to_2d(uncalibrated_image[0], cam_id=cam_id)
            pedestal_2d = geometry_converter.image_1d_to_2d(pedestal[0], cam_id=cam_id)
            gains_2d = geometry_converter.image_1d_to_2d(gain[0], cam_id=cam_id)

        elif cam_id in TWO_CHANNELS_CAMERAS:

            pe_image_2d = geometry_converter.image_1d_to_2d(pe_image, cam_id=cam_id)
            calibrated_image_2d = geometry_converter.image_1d_to_2d(calibrated_image, cam_id=cam_id)

            uncalibrated_image_2d_ch0 = geometry_converter.image_1d_to_2d(uncalibrated_image[0], cam_id=cam_id)
            uncalibrated_image_2d_ch1 = geometry_converter.image_1d_to_2d(uncalibrated_image[1], cam_id=cam_id)
            pedestal_2d_ch0 = geometry_converter.image_1d_to_2d(pedestal[0], cam_id=cam_id)
            pedestal_2d_ch1 = geometry_converter.image_1d_to_2d(pedestal[1], cam_id=cam_id)
            gains_2d_ch0 = geometry_converter.image_1d_to_2d(gain[0], cam_id=cam_id)
            gains_2d_ch1 = geometry_converter.image_1d_to_2d(gain[1], cam_id=cam_id)

        else:
            raise NotImplementedError(geom1d.cam_id)  # TODO

        # Make a mock pixel position array...
        pixel_pos_2d = np.array(np.meshgrid(np.linspace(pixel_pos[0].min(), pixel_pos[0].max(), pe_image_2d.shape[0]),
                                            np.linspace(pixel_pos[1].min(), pixel_pos[1].max(), pe_image_2d.shape[1])))

        # FIX THE ARRAY SHAPE #####################################

        # The ctapipe geometry converter operate on one channel
        # only and then takes and return a 2D array but datapipe
        # fits files keep all channels and thus takes 3D arrays...

        if cam_id in SINGLE_CHANNEL_CAMERAS:
            uncalibrated_image_2d = np.array([uncalibrated_image_2d])
            pedestal_2d =           np.array([pedestal_2d])
            gains_2d =              np.array([gains_2d])
        elif cam_id in TWO_CHANNELS_CAMERAS:
            uncalibrated_image_2d = np.array([uncalibrated_image_2d_ch0, uncalibrated_image_2d_ch1])
            pedestal_2d =           np.array([pedestal_2d_ch0, pedestal_2d_ch1 ])
            gains_2d =              np.array([gains_2d_ch0, gains_2d_ch1])
        else:
            raise NotImplementedError(cam_id)  # TODO

        # GET PIXEL MASK AND PUT NAN IN BLANK PIXELS ##############

        mask_1d = np.ones(pe_image.shape)
        mask_2d = geometry_converter.image_1d_to_2d(mask_1d, cam_id=cam_id)

        # TODO: apparently nan values are already there so this step is useless...

        #calibrated_image_2d[mask_2d != 1] = np.nan
        #pe_image_2d[mask_2d != 1] = np.nan

        #uncalibrated_image_2d[0, mask_2d != 1] = np.nan
        #pedestal_2d[0, mask_2d != 1] = np.nan
        #gains_2d[0, mask_2d != 1] = np.nan

        #if cam_id in ("NectarCam", "LSTCam", "ASTRICam", "ASTRI"):
        #    # Double channel instruments
        #    uncalibrated_image_2d[1, mask_2d != 1] = np.nan
        #    pedestal_2d[1, mask_2d != 1] = np.nan
        #    gains_2d[1, mask_2d != 1] = np.nan

        #pixel_pos_2d[mask_2d != 1] = np.nan

        return Image2D(input_image=calibrated_image_2d,
                       reference_image=pe_image_2d,
                       adc_sum_image=uncalibrated_image_2d,
                       pedestal_image=pedestal_2d,
                       gains_image=gains_2d,
                       pixels_position=pixel_pos_2d,
                       pixels_mask=mask_2d,
                       meta=metadata)


def simtel_images_generator(file_path, tel_filter_list=None, ev_filter_list=None, ctapipe_format=False, **kwargs):
    """
    TODO
    """

    # EXTRACT IMAGES ##########################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.

    source = hessio_event_source(file_path, allowed_tels=tel_filter_list)

    # ITERATE OVER EVENTS #####################################################

    calib = CameraCalibrator(None, None)

    for event in source:

        calib.calibrate(event)  # calibrate the event

        event_id = int(event.dl0.event_id)

        if (ev_filter_list is None) or (event_id in ev_filter_list):

            # ITERATE OVER IMAGES #############################################

            for tel_id in event.trig.tels_with_trigger:

                tel_id = int(tel_id)

                if (tel_filter_list is None) or (tel_id in tel_filter_list):

                    image = simtel_event_to_images(event, tel_id, ctapipe_format=ctapipe_format)

                    # MAKE METADATA ###########################################

                    image.meta['version'] = 1    # Version of the datapipe data format

                    image.meta['tel_id'] = tel_id
                    image.meta['event_id'] = event_id
                    image.meta['file_path'] = file_path
                    image.meta['simtel_path'] = file_path

                    image.meta['num_tel_with_trigger'] = len(event.trig.tels_with_trigger)

                    image.meta['mc_energy'] =  quantity_to_tuple(event.mc.energy, 'TeV')
                    image.meta['mc_azimuth'] = quantity_to_tuple(event.mc.az, 'rad')
                    image.meta['mc_altitude'] = quantity_to_tuple(event.mc.alt, 'rad')
                    image.meta['mc_core_x'] = quantity_to_tuple(event.mc.core_x, 'm')
                    image.meta['mc_core_y'] = quantity_to_tuple(event.mc.core_y, 'm')
                    image.meta['mc_height_first_interaction'] = quantity_to_tuple(event.mc.h_first_int, 'm')

                    image.meta['ev_count'] = int(event.count)

                    image.meta['run_id'] = int(event.dl0.run_id)
                    image.meta['num_tel_with_data'] = len(event.dl0.tels_with_data)

                    image.meta['optical_foclen'] = quantity_to_tuple(event.inst.optical_foclen[tel_id], 'm')
                    image.meta['tel_pos_x'] = quantity_to_tuple(event.inst.tel_pos[tel_id][0], 'm')
                    image.meta['tel_pos_y'] = quantity_to_tuple(event.inst.tel_pos[tel_id][1], 'm')
                    image.meta['tel_pos_z'] = quantity_to_tuple(event.inst.tel_pos[tel_id][2], 'm')

                    # IMAGES ##################################################

                    #images_dict = {}

                    #images_dict["input_image"] = calibrated_image_2d
                    #images_dict["reference_image"] = pe_image_2d
                    #images_dict["adc_sum_image"] = uncalibrated_image_2d
                    #images_dict["pedestal_image"] = pedestal_2d
                    #images_dict["gains_image"] = gains_2d
                    #images_dict["pixels_position"] = pixel_pos_2d
                    #images_dict["pixels_mask"] = mask_2d

                    yield image


# LOAD FITS BENCHMARK IMAGE ##################################################

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

    # METADATA ################################################################

    hdu0 = hdu_list[0]

    metadata_dict = {}

    metadata_dict['version'] = hdu0.header['version']
    metadata_dict['cam_id'] = hdu0.header['cam_id']

    metadata_dict['tel_id'] = hdu0.header['tel_id']
    metadata_dict['event_id'] = hdu0.header['event_id']
    metadata_dict['file_path'] = input_file_path
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
    #metadata_dict['lib_version'] = hdu0.header.comments['lib_version']
    #metadata_dict['argv'] = hdu0.header.comments['argv']
    #metadata_dict['python_version'] = hdu0.header.comments['python']
    #metadata_dict['system'] = hdu0.header.comments['system']

    # IMAGES ##################################################################

    if metadata_dict['version'] == 1:
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
    else:
        raise Exception("Unknown version number")

    # METADATA ################################################################

    metadata_dict['npe'] = float(np.nansum(images_dict["reference_image"]))       # np.sum() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...
    metadata_dict['min_npe'] = float(np.nanmin(images_dict["reference_image"]))   # np.min() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...
    metadata_dict['max_npe'] = float(np.nanmax(images_dict["reference_image"]))   # np.max() returns numpy.int64 objects thus it must be casted with float() to avoid serialization errors with JSON...

    hdu_list.close()

    return images_dict, metadata_dict   # TODO: named tuple


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
    """Write a FITS file containing pe_img, output_file_path and metadata.

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

    hdu.writeto(output_file_path, overwrite=True)  # overwrite=True: overwrite the file if it already exists


###############################################################################

def plot_ctapipe_image(image, geom, figsize=(10, 10), title=None, title_fontsize=24, plot_colorbar=True, plot_axis=True):
    fig = plt.figure(figsize=figsize)
    disp = ctapipe.visualization.CameraDisplay(geom, image=image)
    #disp.enable_pixel_picker()

    if plot_colorbar:
        disp.add_colorbar(fraction=0.04, pad=0.04)
        disp.colorbar.ax.tick_params(labelsize=18)

    if not plot_axis:
        disp.axes.set_axis_off()

    if title is None:
        title = geom.cam_id

    disp.axes.set_title(title, fontsize=title_fontsize)

    return disp

def plot_hillas_parameters_on_axes(ax, image, geom, hillas_params=None, plot_axis_only=False, auto_lim=True, hillas_implementation=2):
    """Plot the shower ellipse and direction on an existing matplotlib axes."""
    if hillas_params is None:
        hillas_params = get_hillas_parameters(geom, image, implementation=hillas_implementation)

    centroid = (hillas_params.cen_x.value, hillas_params.cen_y.value)
    length = hillas_params.length.value
    width = hillas_params.width.value
    angle = hillas_params.psi.to(u.rad).value

    #print("centroid:", centroid)
    #print("length:",   length)
    #print("width:",    width)
    #print("angle:",    angle)

    if not plot_axis_only:
        ellipse = Ellipse(xy=centroid, width=length, height=width, angle=np.degrees(angle), fill=False, color='red', lw=2)
        ax.axes.add_patch(ellipse)

    title = ax.axes.get_title()
    ax.axes.set_title("{} ({:.2f}°)".format(title, np.degrees(angle)))

    # Plot the center of the ellipse

    if not plot_axis_only:
        ax.scatter(*centroid, c="r", marker="x", linewidth=2)

    # Plot the shower ax

    p0_x = centroid[0]
    p0_y = centroid[1]

    p1_x = p0_x + math.cos(angle)
    p1_y = p0_y + math.sin(angle)

    p2_x = p0_x + math.cos(angle + math.pi)
    p2_y = p0_y + math.sin(angle + math.pi)

    ax.plot([p1_x, p2_x], [p1_y, p2_y], ':r', lw=2)

    if not plot_axis_only:
        p3_x = p0_x + math.cos(angle) * length / 2.
        p3_y = p0_y + math.sin(angle) * length / 2.

        ax.plot([p0_x, p3_x], [p0_y, p3_y], '-r')

        p4_x = p0_x + math.cos(angle + math.pi/2.) * width / 2.
        p4_y = p0_y + math.sin(angle + math.pi/2.) * width / 2.

        ax.plot([p0_x, p4_x], [p0_y, p4_y], '-g')

    # Set (back) ax limits

    if auto_lim:
        pixels_position = (geom.pix_x.value, geom.pix_y.value)
        pos_x_min, pos_x_max = np.nanmin(pixels_position[0]), np.nanmax(pixels_position[0])
        pos_y_min, pos_y_max = np.nanmin(pixels_position[1]), np.nanmax(pixels_position[1])

        ax.set_xlim(xmin=pos_x_min)
        ax.set_xlim(xmax=pos_x_max)
        ax.set_ylim(ymin=pos_y_min)
        ax.set_ylim(ymax=pos_y_max)


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

        cmap = COLOR_MAP
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
        if 'mc_energy_unit' in metadata_dict:
            mc_energy = metadata_dict['mc_energy']
            mc_energy_unit = metadata_dict['mc_energy_unit']
        else:
            mc_energy = metadata_dict['mc_energy'][0]
            mc_energy_unit = metadata_dict['mc_energy'][1]

        main_title = "{} (Tel. {}, Ev. {}) {:.2E}{}".format(os.path.basename(metadata_dict['simtel_path']),
                                                            metadata_dict['tel_id'],
                                                            metadata_dict['event_id'],
                                                            mc_energy,
                                                            mc_energy_unit)
    else:
        main_title = ""

    _plot_list(img_list, title_list, main_title)
    plt.show()


def mpl_save_list(img_list, output_file_path, title_list, metadata_dict=None):
    """
    img should be a list of 2D numpy array.
    """

    # Main title
    if metadata_dict is not None:
        if 'mc_energy_unit' in metadata_dict:
            mc_energy = metadata_dict['mc_energy']
            mc_energy_unit = metadata_dict['mc_energy_unit']
        else:
            mc_energy = metadata_dict['mc_energy'][0]
            mc_energy_unit = metadata_dict['mc_energy'][1]

        main_title = "{} (Tel. {}, Ev. {}) {:.2E}{}".format(os.path.basename(metadata_dict['simtel_path']),
                                                            metadata_dict['tel_id'],
                                                            metadata_dict['event_id'],
                                                            mc_energy,
                                                            mc_energy_unit)
    else:
        main_title = ""

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
