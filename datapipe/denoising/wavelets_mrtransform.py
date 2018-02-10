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
Denoise FITS and PNG images with Wavelet Transform.

This script use mr_transform -- a program written CEA/CosmoStat
(www.cosmostat.org) -- to make Wavelet Transform.

It originally came from
https://github.com/jdhp-sap/snippets/blob/master/mr_transform/mr_transform_wrapper_denoising.py.

Examples
--------
  ./denoising_with_wavelets_mr_transform.py -h
  ./denoising_with_wavelets_mr_transform.py ./test.fits
  ipython3 -- ./denoising_with_wavelets_mr_transform.py -n4 ./test.fits

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
                      noise_distribution=None,
                      debug=False):
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
    debug : bool, optional
        Do debug plots and prints if `True`.

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

    input_file_name = ".tmp_{}_{}_in.fits".format(os.getpid(), time.time())
    input_file_path = os.path.join(tmp_files_directory, input_file_name)

    output_file_name = ".tmp_{}_{}_out.fits".format(os.getpid(), time.time())
    mr_output_file_path = os.path.join(tmp_files_directory, output_file_name)

    # INJECT NOISE IN NAN PIXELS ###########################

    # TODO: should this noise injection be done in the abstract 'rum()' function ?

    # See https://stackoverflow.com/questions/29365194/replacing-missing-values-with-random-in-a-numpy-array
    nan_mask = np.isnan(input_image)

    if debug:  # TODO: remove this, use notebooks instead...
        print(input_image)
        images.plot(input_image, "In")
        images.plot(nan_mask, "Mask")

    if noise_distribution is not None:
        nan_noise_size = np.count_nonzero(nan_mask)
        input_image[nan_mask] = noise_distribution.rvs(size=nan_noise_size)

    if debug:  # TODO: remove this, use notebooks instead...
        print(input_image)
        images.plot(input_image, "Noise injected")

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
    
    return wavelet_planes


def filter_planes(wavelet_planes,
                  method='hard_filtering',
                  thresholds=None,
                  detect_only_positive_structure=False,
                  debug=False):
                  #**kwargs):
    """Filter the wavelet planes.
    
    Parameters
    ----------
    wavelet_planes : list of array_like
        The wavelet planes to filter.
    method : str, optional
        The filtering method to use. So far, only the 'hard_filtering' and
        'ksigma_hard_filtering' methods are implemented.
    debug : bool, optional
        Do debug plots and prints if `True`.

    Returns
    -------
    list
        Return a list containing the filtered wavelet planes.
    """
    filtered_wavelet_planes = copy.deepcopy(wavelet_planes)

    # The last plane should be kept unmodified

    for plane_index, plane in enumerate(wavelet_planes[0:-1]):

        if method == 'hard_filtering':

            if detect_only_positive_structure:
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

            if detect_only_positive_structure:
                plane_mask = plane > (plane_noise_std * thresholds[plane_index])
            else:
                plane_mask = abs(plane) > (plane_noise_std * thresholds[plane_index])  

            filtered_plane = plane * plane_mask

        else:

            raise ValueError('Unknown method "{}". Should be "hard_filtering" or "ksigma_hard_filtering".'.format(method))

        filtered_wavelet_planes[plane_index] = filtered_plane

        if debug:  # TODO: remove this, use notebooks instead...
            images.plot(plane, title="Plane {}".format(plane_index))
            images.plot(plane_mask, title="Binary mask for plane {}".format(plane_index))
            images.plot(filtered_plane, title="Filtered plane {}".format(plane_index))

    return filtered_wavelet_planes


def inverse_wavelet_transform(wavelet_planes,
                              last_plane='keep',
                              debug=False):
    """Compute the inverse wavelet transform of `wavelet_planes`.

    Parameters
    ----------
    wavelet_planes : list of array_like
        The wavelet planes to (inverse) transform.
    last_plane : str, optional
        Define what to do with the last plane: 'keep' to keep it in the inverse
        transform, 'drop' to remove it in the inverse transform, 'mask' to keep
        only pixels that are *significant* in the others planes.
    debug : bool, optional
        Do debug plots and prints if `True`.

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
        output_image += plane[-1]
    elif last_plane == "mask":
        # Only keep last plane's pixels that are *significant* in the others planes
        significant_pixels_mask = np.zeros(wavelet_planes[0].shape)
        for plane in wavelet_planes[0:-1]:
            significant_pixels_mask[plane > 0] = 1
        output_image += plane[-1] * significant_pixels_mask

    return output_image


class WaveletTransform(AbstractCleaningAlgorithm):
    """TODO"""

    def __init__(self):
        super().__init__()
        self.label = "WT (mr_transform)"  # Name to show in plots

    def clean_image(self,
                    input_img,
                    type_of_filtering=None,
                    number_of_scales=4,
                    suppress_last_scale=False,
                    kill_isolated_pixels=False,
                    filter_thresholds=None,
                    detect_only_positive_structure=False,
                    noise_distribution=None,
                    tmp_files_directory=".",
                    output_data_dict=None,
                    debug=False,
                    **kwargs):
        """Clean the `input_img` image.

        Apply the wavelet transform, filter planes and return the reverse
        transformed image.

        mr_filter
        -K 
        -k
        -F2
        -C1
        -s3
        -m2  (a essayer ou -m10)

        eventuellement -w pour le debug
        """

        wavelet_planes = wavelet_transform(input_img,
                                           number_of_scales=number_of_scales,
                                           tmp_files_directory=tmp_files_directory,
                                           noise_distribution=noise_distribution,
                                           debug=debug)

        filtered_wavelet_planes = filter_planes(wavelet_planes[0:-1],
                                                debug=debug)
        filtered_wavelet_planes.append(wavelet_planes[-1])     # Append the last (unfiltered) plane

        cleaned_image = inverse_wavelet_transform(filtered_wavelet_planes,
                                                  debug=debug)

        # KILL ISOLATED PIXELS #################################

        img_cleaned_islands_delta_pe, img_cleaned_islands_delta_abs_pe, img_cleaned_islands_delta_num_pixels = kill_isolated_pixels_stats(cleaned_img)
        img_cleaned_num_islands = number_of_islands(cleaned_img)

        if output_data_dict is not None:
            output_data_dict["img_cleaned_islands_delta_pe"] = img_cleaned_islands_delta_pe
            output_data_dict["img_cleaned_islands_delta_abs_pe"] = img_cleaned_islands_delta_abs_pe
            output_data_dict["img_cleaned_islands_delta_num_pixels"] = img_cleaned_islands_delta_num_pixels
            output_data_dict["img_cleaned_num_islands"] = img_cleaned_num_islands

        if kill_isolated_pixels:
            if verbose:
                print("Kill isolated pixels")
            initial_time = time.perf_counter()
            cleaned_img = scipy_kill_isolated_pixels(cleaned_img)
            exec_time_sec = time.perf_counter() - initial_time
            if output_data_dict is not None:
                output_data_dict["scipy_kill_isolated_pixels_time_sec"] = exec_time_sec

        return cleaned_image


def main():
    """The main module execution function.

    Contains the instructions executed when the module is not imported but
    directly called from the system command line.
    """

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser.add_argument("--type-of-filtering", "-f", metavar="STRING",
                        help="""Type of filtering:
                            'hard_filtering': Multiresolution Hard Thresholding
                            'ksigma_hard_filtering': Multiresolution Hard K-Sigma Thresholding""")

    parser.add_argument("--number-of-scales", "-n", type=int, metavar="integer",
                        help="Number of scales used in the multiresolution transform. Default=4.")

    parser.add_argument("--filter-thresholds", "-s", metavar="FLOAT LIST",
                        help="Thresholds used for the plane filtering.")

    parser.add_argument("--suppress-last-scale", "-K", action="store_true",
                        help="Suppress the last scale (to have background pixels = 0)")

    parser.add_argument("--detect-only-positive-structure", "-p", action="store_true",
                        help="Detect only positive structure")

    parser.add_argument("--kill-isolated-pixels", action="store_true",
                        help="Suppress isolated pixels in the support (scipy implementation)")

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
    number_of_scales = args.number_of_scales
    suppress_last_scale = args.suppress_last_scale    # TODO
    kill_isolated_pixels = args.kill_isolated_pixels
    filter_thresholds_str = args.filter_thresholds
    detect_only_positive_structure = args.detect_only_positive_structure
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

    filter_thresholds = [float(threshold_str) for threshold_str in filter_thresholds_str.split(",")]

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
            "number_of_scales": number_of_scales,
            "suppress_last_scale": suppress_last_scale,
            "kill_isolated_pixels": kill_isolated_pixels,
            "filter_thresholds": filter_thresholds,
            "detect_only_positive_structure": detect_only_positive_structure,
            "noise_distribution": noise_distribution,
            "verbose": verbose,
            "tmp_files_directory": tmp_dir
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

