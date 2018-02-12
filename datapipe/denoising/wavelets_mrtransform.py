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

"""Denoise FITS and PNG images with Wavelet Transform.

This script use mr_transform -- a program written CEA/CosmoStat
(www.cosmostat.org) -- to make Wavelet Transform.

Usage
-----

    wavelets_mrtransform.py [-h] [--type-of-filtering STRING]
                                 [--filter-thresholds FLOAT LIST]
                                 [--last-scale STRING]
                                 [--detect-only-positive-structures]
                                 [--kill-isolated-pixels]
                                 [--noise-cdf-file FILE] [--tmp-dir DIRECTORY]
                                 [--verbose] [--debug] [--max-images INTEGER]
                                 [--telid INTEGER] [--eventid INTEGER]
                                 [--camid STRING] [--benchmark STRING]
                                 [--label STRING] [--plot] [--saveplot FILE]
                                 [--output FILE]
                                 FILE [FILE ...]

    Denoise FITS images with Wavelet Transform.

    positional arguments:
      FILE                  The files image to process (FITS).If fileargs is a
                            directory,all FITS files it contains are processed.

    optional arguments:
      -h, --help            show this help message and exit
      --type-of-filtering STRING, -f STRING
                            Type of filtering: hard_filtering,
                            ksigma_hard_filtering
      --filter-thresholds FLOAT LIST, -t FLOAT LIST
                            Thresholds used for the plane filtering.
      --last-scale STRING, -L STRING
                            Last plane treatment: keep, drop, mask
      --detect-only-positive-structures, -p
                            Detect only positive structure
      --kill-isolated-pixels
                            Suppress isolated pixels in the support (scipy
                            implementation)
      --noise-cdf-file FILE
                            The JSON file containing the Cumulated Distribution
                            Function of the noise model used to inject artificial
                            noise in blank pixels (those with a NaN value).
                            Default=None.
      --tmp-dir DIRECTORY   The directory where temporary files are written.
      --verbose, -v         Verbose mode
      --debug               Debug mode
      --max-images INTEGER  The maximum number of images to process
      --telid INTEGER       Only process images from the specified telescope
      --eventid INTEGER     Only process images from the specified event
      --camid STRING        Only process images from the specified camera
      --benchmark STRING, -b STRING
                            The benchmark method to use to assess the algorithm
                            for thegiven images
      --label STRING, -l STRING
                            The label attached to the produced results
      --plot                Plot images
      --saveplot FILE       The output file where to save plotted images
      --output FILE, -o FILE
                            The output file path (JSON)

Examples
--------
  ./wavelets_mrtransform.py -h
  ./wavelets_mrtransform.py ./test.fits
  ipython3 -- ./wavelets_mrtransform.py -t 21.5,11.7 ./test.fits

Notes
-----
This script requires the mr_transform program
(http://www.cosmostat.org/software/isap/).

It also requires Numpy and Matplotlib Python libraries.
"""

__all__ = ['wavelet_transform',
           'filter_planes',
           'inverse_wavelet_transform',
           'clean_image']

import argparse
import copy
import numpy as np
import os
import time

from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from datapipe.denoising.inverse_transform_sampling import EmpiricalDistribution
from datapipe.io import images

from datapipe.image.kill_isolated_pixels import kill_isolated_pixels as scipy_kill_isolated_pixels
from datapipe.image.kill_isolated_pixels import kill_isolated_pixels_stats
from datapipe.image.kill_isolated_pixels import number_of_islands

# CONSTANTS ##################################################################

DEBUG = False

AVAILABLE_TYPE_OF_FILTERING = ('hard_filtering', 'ksigma_hard_filtering')
AVAILABLE_LAST_SCALE_OPTIONS = ('keep', 'drop', 'mask')

DEFAULT_TYPE_OF_FILTERING = 'hard_filtering'
DEFAULT_FILTER_THRESHOLDS_STR = '0,0'            # TODO: change the default value...
DEFAULT_FILTER_THRESHOLDS = [float(threshold_str) for threshold_str in DEFAULT_FILTER_THRESHOLDS_STR.split(",")]
DEFAULT_LAST_SCALE_TREATMENT = 'mask'

# EXCEPTIONS #################################################################

class MrTransformError(Exception):
    """Common `wavelet_mrtransform` module's error."""
    pass

class WrongDimensionError(MrTransformError):
    """Raised when data having a wrong number of dimensions is given.

    Attributes
    ----------
    msg : str
        Explanation of the error.
    """

    def __init__(self, msg=None):
        if msg is None:
            self.msg = "The data has a wrong number of dimension."


##############################################################################

def wavelet_transform(input_image,
                      number_of_scales=4,
                      tmp_files_directory=".",
                      noise_distribution=None):
    """Compute the wavelet transform of `input_image`.

    Parameters
    ----------
    input_image : array_like
        The input image to transform.
    number_of_scales : int, optional
        The number of scales used to transform `input_image` or in other words
        the number of wavelet planes returned.
    tmp_files_directory : str, optional
        The path of the directory used to store mr_transform temporary data.
        The default is the current directory, but it may be more appropriate to
        specify here the path of a directory mounted in a ramdisk to speedup
        I/Os ("/Volumes/ramdisk" on MacOSX or "/dev/shm" on Linux).
    noise_distribution : `EmpiricalDistribution`, optional
        The noise distribution used to fill 'empty' NaN pixels with the
        appropriate random noise distribution. If none, NaN pixels are fill
        with zeros (which may add unwanted harmonics in wavelet planes).

    Returns
    -------
    list
        Return a list containing the `number_of_scales` wavelet planes.

    Raises
    ------
    WrongDimensionError
        If `input_image` is not a 2D array.
    """

    input_image = input_image.copy()

    if input_image.ndim != 2:
        msg = "The data should be a 2D array."
        raise WrongDimensionError(msg)

    # INJECT NOISE IN NAN PIXELS ###########################################

    # TODO: should this noise injection be done in the abstract 'run()' function ?

    # See https://stackoverflow.com/questions/29365194/replacing-missing-values-with-random-in-a-numpy-array

    if noise_distribution is not None:
        nan_mask = np.isnan(input_image)

        if DEBUG:
            print(input_image)
            images.plot(input_image, "In")
            images.plot(nan_mask, "Mask")

        nan_noise_size = np.count_nonzero(nan_mask)
        input_image[nan_mask] = noise_distribution.rvs(size=nan_noise_size)

        if DEBUG:
            print(input_image)
            images.plot(input_image, "Noise injected")

    # DO THE WAVELET TRANSFORM #############################################

    input_file_name = ".tmp_{}_{}_in.fits".format(os.getpid(), time.time())
    input_file_path = os.path.join(tmp_files_directory, input_file_name)

    output_file_name = ".tmp_{}_{}_out.fits".format(os.getpid(), time.time())
    mr_output_file_path = os.path.join(tmp_files_directory, output_file_name)

    try:
        # WRITE THE INPUT FILE (FITS) ##########################

        images.save_fits(input_image, input_file_path)

        # EXECUTE MR_TRANSFORM #################################

        cmd = 'mr_transform -n{} "{}" {}'.format(number_of_scales,
                                                 input_file_path,
                                                 mr_output_file_path)
        os.system(cmd)

        cmd = "mv {}.mr {}".format(mr_output_file_path, mr_output_file_path)
        os.system(cmd)

        # READ THE MR_TRANSFORM OUTPUT FILE ####################

        wavelet_planes = images.load_fits(mr_output_file_path, 0)

        # CHECK RESULT #########################################

        if wavelet_planes.ndim != 3:
            msg = "Unexpected error: the output FITS file should contain a 3D array."
            raise WrongDimensionError(msg)

    finally:

        # REMOVE FITS FILES ####################################

        os.remove(input_file_path)
        os.remove(mr_output_file_path)

    wavelet_planes_list = [plane for plane in wavelet_planes]

    # INJECT NOISE IN NAN: PUT BACK NAN VALUES #############

    if noise_distribution is not None:
        for plane in wavelet_planes_list:
            plane[nan_mask] = np.nan

    return wavelet_planes_list


def filter_planes(wavelet_planes,
                  method=DEFAULT_TYPE_OF_FILTERING,
                  thresholds=DEFAULT_FILTER_THRESHOLDS,
                  detect_only_positive_structures=False):
                  #**kwargs):
    """Filter the wavelet planes.

    The last plane (called residuals) is kept unmodified.
    
    Parameters
    ----------
    wavelet_planes : list of array_like
        The wavelet planes to filter, including the last *residual* plane.
    method : str, optional
        The filtering method to use. So far, only the 'hard_filtering' and
        'ksigma_hard_filtering' methods are implemented.
    thresholds : list of float
        Thresholds used for the plane filtering.
    detect_only_positive_structures : bool
        Detect only positive structures.

    Returns
    -------
    list
        Return a list containing the filtered wavelet planes.
    """
    filtered_wavelet_planes = copy.deepcopy(wavelet_planes)

    # The last plane is kept unmodified

    for plane_index, plane in enumerate(wavelet_planes[0:-1]):

        if method == 'hard_filtering':

            if detect_only_positive_structures:
                plane_mask = plane > thresholds[plane_index]
            else:
                plane_mask = abs(plane) > thresholds[plane_index]

            filtered_plane = plane * plane_mask

        elif method == 'ksigma_hard_filtering':

            # Compute the standard deviation of the plane ##

            plane_noise_std = np.std(plane)  # TODO: this is wrong... it should be the estimated std of the **noise**

            # Apply a threshold on the plane ###############

            # Remark: "abs(plane) > (plane_noise_std * 3.)" should be the correct way to
            # make the image mask, but sometimes results looks better when all
            # negative coefficients are dropped ("plane > (plane_noise_std * 3.)")

            if detect_only_positive_structures:
                plane_mask = plane > (plane_noise_std * thresholds[plane_index])
            else:
                plane_mask = abs(plane) > (plane_noise_std * thresholds[plane_index])  

            filtered_plane = plane * plane_mask

        else:

            raise ValueError('Unknown method "{}". Should be "hard_filtering" or "ksigma_hard_filtering".'.format(method))

        filtered_wavelet_planes[plane_index] = filtered_plane

        if DEBUG:
            images.plot(plane, title="Plane {}".format(plane_index))
            images.plot(plane_mask, title="Binary mask for plane {}".format(plane_index))
            images.plot(filtered_plane, title="Filtered plane {}".format(plane_index))

    return filtered_wavelet_planes


def inverse_wavelet_transform(wavelet_planes,
                              last_plane=DEFAULT_LAST_SCALE_TREATMENT):
    """Compute the inverse wavelet transform of `wavelet_planes`.

    Parameters
    ----------
    wavelet_planes : list of array_like
        The wavelet planes to (inverse) transform.
    last_plane : str, optional
        Define what to do with the last plane: 'keep' to keep it in the inverse
        transform, 'drop' to remove it in the inverse transform, 'mask' to keep
        only pixels that are *significant* in the others planes.

    Returns
    -------
    array_like
        Return the cleaned image.
    """
    output_image = np.zeros(wavelet_planes[0].shape)

    for plane in wavelet_planes[0:-1]:
        # Sum all planes except the last one (residuals plane)
        output_image += plane

    # Apply a special treatment with the last plane (residuals plane)
    if last_plane == "keep":

        # Keep the last plane
        output_image += wavelet_planes[-1]

    elif last_plane == "mask":

        # Only keep last plane's pixels that are *significant* in the others planes
        significant_pixels_mask = np.zeros(wavelet_planes[0].shape)
        for plane in wavelet_planes[0:-1]:
            significant_pixels_mask[plane != 0] = 1
        output_image += wavelet_planes[-1] * significant_pixels_mask

    return output_image


class WaveletTransform(AbstractCleaningAlgorithm):
    """The wavelet transform wrapper for ctapipe."""

    def __init__(self):
        super().__init__()
        self.label = "WT (mr_transform)"  # Name to show in plots

    def clean_image(self,
                    input_image,
                    type_of_filtering=DEFAULT_TYPE_OF_FILTERING,
                    filter_thresholds=DEFAULT_FILTER_THRESHOLDS,
                    last_scale_treatment=DEFAULT_LAST_SCALE_TREATMENT,
                    detect_only_positive_structures=False,
                    kill_isolated_pixels=False,
                    noise_distribution=None,
                    tmp_files_directory=".",
                    output_data_dict=None,
                    **kwargs):
        """Clean the `input_image` image.

        Apply the wavelet transform, filter planes and return the reverse
        transformed image.

        Parameters
        ----------
        input_image : array_like
            The image to clean.
        type_of_filtering : str
            Type of filtering: 'hard_filtering' or 'ksigma_hard_filtering'.
        filter_thresholds : list of float
            Thresholds used for the plane filtering.
        last_scale_treatment : str
            Last plane treatment: 'keep', 'drop' or 'mask'.
        detect_only_positive_structures : bool
            Detect only positive structures.
        kill_isolated_pixels : bool
            Suppress isolated pixels in the support.
        noise_distribution : bool
            The JSON file containing the Cumulated Distribution Function of the
            noise model used to inject artificial noise in blank pixels (those
            with a NaN value).
        tmp_files_directory : str
            The path of the directory where temporary files are written.
        output_data_dict : dict
            A dictionary used to return results and intermediate results.

        Returns
        -------
            Return the cleaned image.
        """

        if DEBUG:
            print("Filter thresholds:", filter_thresholds)

        number_of_scales = len(filter_thresholds) + 1

        if DEBUG:
            print("Number of scales:", number_of_scales)

        # COMPUTE THE WAVELET TRANSFORM #######################################

        wavelet_planes = wavelet_transform(input_image,
                                           number_of_scales=number_of_scales,
                                           tmp_files_directory=tmp_files_directory,
                                           noise_distribution=noise_distribution)

        if DEBUG:
            for index, plane in enumerate(wavelet_planes):
                images.plot(plane, "Plane " + str(index))

        # FILTER WAVELET PLANES ###############################################

        filtered_wavelet_planes = filter_planes(wavelet_planes,
                                                method=type_of_filtering,
                                                thresholds=filter_thresholds,
                                                detect_only_positive_structures=detect_only_positive_structures)

        #if DEBUG:
        #    for index, plane in enumerate(filtered_wavelet_planes):
        #        images.plot(plane, "Filtered plane " + str(index))

        # COMPUTE THE INVERSE TRANSFORM #######################################

        cleaned_image = inverse_wavelet_transform(filtered_wavelet_planes,
                                                  last_plane=last_scale_treatment)
        if DEBUG:
            images.plot(cleaned_image, "Cleaned image")

        # KILL ISOLATED PIXELS ################################################

        kill_islands = kill_isolated_pixels_stats(cleaned_image)
        img_cleaned_islands_delta_pe, img_cleaned_islands_delta_abs_pe, img_cleaned_islands_delta_num_pixels = kill_islands
        img_cleaned_num_islands = number_of_islands(cleaned_image)

        if output_data_dict is not None:
            output_data_dict["img_cleaned_islands_delta_pe"] = img_cleaned_islands_delta_pe
            output_data_dict["img_cleaned_islands_delta_abs_pe"] = img_cleaned_islands_delta_abs_pe
            output_data_dict["img_cleaned_islands_delta_num_pixels"] = img_cleaned_islands_delta_num_pixels
            output_data_dict["img_cleaned_num_islands"] = img_cleaned_num_islands

        if kill_isolated_pixels:
            cleaned_image = scipy_kill_isolated_pixels(cleaned_image)
            if DEBUG:
                images.plot(cleaned_image, "Cleaned image after island kill")

        return cleaned_image


def main():
    """The main module execution function.

    Contains the instructions executed when the module is not imported but
    directly called from the system command line.
    """

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--type-of-filtering", "-f", metavar="STRING", default=DEFAULT_TYPE_OF_FILTERING,
                        help="Type of filtering: {}.".format(", ".join(AVAILABLE_TYPE_OF_FILTERING)))

    parser.add_argument("--filter-thresholds", "-t", metavar="FLOAT LIST", default=DEFAULT_FILTER_THRESHOLDS_STR,
                        help="Thresholds used for the plane filtering.")

    parser.add_argument("--last-scale", "-L", metavar="STRING", default=DEFAULT_LAST_SCALE_TREATMENT,
                        help="Last plane treatment: {}.".format(", ".join(AVAILABLE_LAST_SCALE_OPTIONS)))

    parser.add_argument("--detect-only-positive-structures", "-p", action="store_true",
                        help="Detect only positive structures.")

    parser.add_argument("--kill-isolated-pixels", action="store_true",
                        help="Suppress isolated pixels in the support (scipy implementation).")

    parser.add_argument("--noise-cdf-file", metavar="FILE",
                        help="The JSON file containing the Cumulated Distribution Function of the noise model used to inject artificial noise in blank pixels (those with a NaN value). Default=None.")

    parser.add_argument("--tmp-dir", default=".", metavar="DIRECTORY",
                        help="The directory where temporary files are written.")

    # COMMON OPTIONS

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    parser.add_argument("--debug", action="store_true",
                        help="Debug mode")

    parser.add_argument("--max-images", type=int, metavar="INTEGER", 
                        help="The maximum number of images to process")

    parser.add_argument("--telid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified telescope")

    parser.add_argument("--eventid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified event")

    parser.add_argument("--camid", metavar="STRING", 
                        help="Only process images from the specified camera")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--label", "-l", default=None,
                        metavar="STRING",
                        help="The label attached to the produced results")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", default=None, metavar="FILE",
                        help="The output file where to save plotted images")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    type_of_filtering = args.type_of_filtering
    filter_thresholds_str = args.filter_thresholds
    last_scale_treatment = args.last_scale
    detect_only_positive_structures = args.detect_only_positive_structures
    kill_isolated_pixels = args.kill_isolated_pixels
    noise_cdf_file = args.noise_cdf_file
    tmp_dir = args.tmp_dir

    verbose = args.verbose
    debug = args.debug
    max_images = args.max_images
    tel_id = args.telid
    event_id = args.eventid
    cam_id = args.camid
    benchmark_method = args.benchmark
    label = args.label
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    # CHECK OPTIONS #############################

    if type_of_filtering not in AVAILABLE_TYPE_OF_FILTERING:
        raise ValueError('Unknown type of filterning: "{}". Should be in {}'.format(type_of_filtering,
                                                                                    AVAILABLE_TYPE_OF_FILTERING))

    try:
        filter_thresholds = [float(threshold_str) for threshold_str in filter_thresholds_str.split(",")]
    except:
        raise ValueError('Wrong filter thresholds: "{}". Should be in a list of figures separated by a comma (e.g. "3,2,3")'.format(filter_thresholds_str))

    if last_scale_treatment not in AVAILABLE_LAST_SCALE_OPTIONS:
        raise ValueError('Unknown type of last scale treatment: "{}". Should be in {}'.format(last_scale_treatment ,
                                                                                              AVAILABLE_LAST_SCALE_OPTIONS))

    # TODO: check the noise_cdf_file value
    # TODO: check the tmp_dir value

    #############################################

    if args.output is None:
        output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    if noise_cdf_file is not None:
        noise_distribution = EmpiricalDistribution(noise_cdf_file)
    else:
        noise_distribution = None

    cleaning_function_params = {
            "type_of_filtering": type_of_filtering,
            "filter_thresholds": filter_thresholds,
            "last_scale_treatment": last_scale_treatment,
            "detect_only_positive_structures": detect_only_positive_structures,
            "kill_isolated_pixels": kill_isolated_pixels,
            "noise_distribution": noise_distribution,
            "tmp_files_directory": tmp_dir,
            "verbose": verbose
        }

    cleaning_algorithm = WaveletTransform()

    if verbose:
        cleaning_algorithm.verbose = True

    if label is not None:
        cleaning_algorithm.label = label

    output_dict = cleaning_algorithm.run(cleaning_function_params,
                                         input_file_or_dir_path_list,
                                         benchmark_method,
                                         output_file_path,
                                         plot=plot,
                                         saveplot=saveplot,
                                         max_num_img=max_images,
                                         tel_id=tel_id,
                                         event_id=event_id,
                                         cam_id=cam_id,
                                         debug=debug)

if __name__ == "__main__":
    main()

