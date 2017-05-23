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
... TODO
"""

__all__ = ['extract_images']

import argparse
from astropy.io import fits
import datetime
import numpy as np
import os
import sys

import ctapipe
from ctapipe.io.hessio import hessio_event_source
import pyhessio

from datapipe.io import images
from datapipe.io import geometry_converter
import datapipe.io.montecarlo_calibration_gct as mc_calibration

from datapipe import __version__ as VERSION

DEFAULT_TEL_FILTER = list(range(1, 32))   # TODO


def extract_images(simtel_file_path,
                   tel_id_filter_list=None,
                   event_id_filter_list=None,
                   output_directory=None):

    # EXTRACT IMAGES ##########################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=tel_id_filter_list)

    # ITERATE OVER EVENTS #####################################################

    for event in source:

        event_id = int(event.dl0.event_id)

        if (event_id_filter_list is None) or (event_id in event_id_filter_list):

            #print("event", event_id)

            # ITERATE OVER IMAGES #############################################

            for tel_id in event.trig.tels_with_trigger:

                tel_id = int(tel_id)

                if tel_id in tel_id_filter_list:

                    #print("telescope", tel_id)

                    # CHECK THE IMAGE GEOMETRY (GCT ONLY) ###################

                    # TODO

                    #print("checking geometry")

                    x, y = event.inst.pixel_pos[tel_id]
                    foclen = event.inst.optical_foclen[tel_id]
                    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

                    if (geom.pix_type != "rectangular") or (geom.cam_id != "GCT"):
                        raise ValueError("Telescope {}: error (the input image is not a valide GCT telescope image)".format(tel_id))

                    # GET IMAGES ##############################################

                    pe_image = event.mc.tel[tel_id].photo_electron_image   # 1D np array

                    # uncalibrated_image = [1D numpy array of channel1, 1D numpy array of channel2]
                    # calibrated_image = 1D numpy array

                    #uncalibrated_image = event.dl0.tel[tel_id].adc_sums  # ctapipe 0.3.0
                    uncalibrated_image = event.r0.tel[tel_id].adc_sums    # ctapipe 0.4.0
                    pedestal = event.mc.tel[tel_id].pedestal
                    gain = event.mc.tel[tel_id].dc_to_pe
                    pixel_pos = event.inst.pixel_pos[tel_id]

                    #print("calibrating")

                    calibrated_image = mc_calibration.apply_mc_calibration(uncalibrated_image, pedestal, gain)

                    # CROP IMAGE ##############################################

                    #print("cropping ADC image")

                    cropped_adc_sums = geometry_converter.gct_to_3d_array(uncalibrated_image)

                    #print("cropping PE image")

                    cropped_pe_img = geometry_converter.gct_to_2d_array(pe_image)

                    #print("cropping calibrated image")

                    cropped_img = geometry_converter.gct_to_2d_array(calibrated_image)

                    #print("cropping pedestal and gain")

                    cropped_pedestal = geometry_converter.gct_to_3d_array(pedestal)
                    cropped_gains = geometry_converter.gct_to_3d_array(gain)

                    #print("cropping pixel positions")

                    cropped_pixel_pos = geometry_converter.gct_to_3d_array(pixel_pos)

                    # GET PIXEL MASK ##########################################

                    pixel_mask = geometry_converter.gct_pixel_mask()

                    # MAKE METADATA ###########################################

                    metadata = {}

                    metadata['version'] = 1    # Version of the datapipe fits format

                    metadata['cam_id'] = "GCT"

                    metadata['tel_id'] = tel_id
                    metadata['event_id'] = event_id
                    metadata['simtel'] = simtel_file_path

                    metadata['tel_trig'] = len(event.trig.tels_with_trigger)

                    metadata['energy'] =  quantity_to_tuple(event.mc.energy, 'TeV')
                    metadata['mc_az'] = quantity_to_tuple(event.mc.az, 'rad')
                    metadata['mc_alt'] = quantity_to_tuple(event.mc.alt, 'rad')
                    metadata['mc_corex'] = quantity_to_tuple(event.mc.core_x, 'm')
                    metadata['mc_corey'] = quantity_to_tuple(event.mc.core_y, 'm')
                    metadata['mc_hfi'] = quantity_to_tuple(event.mc.h_first_int, 'm')

                    metadata['count'] = int(event.count)
                    
                    metadata['run_id'] = int(event.dl0.run_id)
                    metadata['tel_data'] = len(event.dl0.tels_with_data)

                    metadata['foclen'] = quantity_to_tuple(event.inst.optical_foclen[tel_id], 'm')
                    metadata['tel_posx'] = quantity_to_tuple(event.inst.tel_pos[tel_id][0], 'm')
                    metadata['tel_posy'] = quantity_to_tuple(event.inst.tel_pos[tel_id][1], 'm')
                    metadata['tel_posz'] = quantity_to_tuple(event.inst.tel_pos[tel_id][2], 'm')

                    # TODO: Astropy fails to store the following data in FITS files
                    #metadata['uid'] = os.getuid()
                    #metadata['datetime'] = str(datetime.datetime.now())
                    #metadata['version'] = VERSION
                    #metadata['argv'] = " ".join(sys.argv).encode('ascii', errors='ignore').decode('ascii')
                    #metadata['python'] = " ".join(sys.version.splitlines()).encode('ascii', errors='ignore').decode('ascii')
                    #metadata['system'] = " ".join(os.uname())

                    # SAVE THE IMAGE ##########################################

                    output_file_path_template = "{}_TEL{:03d}_EV{:05d}.fits"

                    if output_directory is not None:
                        simtel_basename = os.path.basename(simtel_file_path)
                        prefix = os.path.join(output_directory, simtel_basename)
                    else:
                        prefix = simtel_file_path

                    output_file_path = output_file_path_template.format(prefix,
                                                                        tel_id,
                                                                        event_id)

                    print("saving", output_file_path)

                    images.save_benchmark_images(img = cropped_img,
                                                 pe_img = cropped_pe_img,
                                                 adc_sums_img = cropped_adc_sums,
                                                 pedestal_img = cropped_pedestal,
                                                 gains_img = cropped_gains,
                                                 pixel_pos = cropped_pixel_pos,
                                                 pixel_mask = pixel_mask,
                                                 metadata = metadata,
                                                 output_file_path = output_file_path)


def quantity_to_tuple(quantity, unit_str):
    """
    Splits a quantity into a tuple of (value,unit) where unit is FITS complient.

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


def main():

    # PARSE OPTIONS ###########################################################

    desc = "Generate FITS files compliant for cleaning benchmark (from simtel files)."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t",
                        metavar="INTEGER LIST",
                        help="The telescopes to query (telescopes number separated by a comma)")

    parser.add_argument("--event", "-e",
                        metavar="INTEGER LIST",
                        help="The events to extract (events ID separated by a comma)")

    parser.add_argument("--output", "-o",
                        metavar="DIRECTORY",
                        help="The output directory")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The simtel files to process")

    args = parser.parse_args()

    if args.telescope is None:
        tel_id_filter_list = DEFAULT_TEL_FILTER
    else:
        tel_id_filter_list = [int(tel_id_str) for tel_id_str in args.telescope.split(",")]

    if args.event is None:
        event_id_filter_list = None
    else:
        event_id_filter_list = [int(event_id_str) for event_id_str in args.event.split(",")]

    print("Telescopes:", tel_id_filter_list)
    print("Events:", event_id_filter_list)

    output_directory = args.output
    simtel_file_path_list = args.fileargs

    if output_directory is not None:
        if not (os.path.exists(output_directory) and os.path.isdir(output_directory)):
            raise Exception("{} does not exist or is not a directory.".format(output_directory))

    # ITERATE OVER SIMTEL FILES ###############################################

    for simtel_file_path in simtel_file_path_list:

        print("Processing", simtel_file_path)

        # EXTRACT, CROP AND SAVE THE IMAGES ###################################

        extract_images(simtel_file_path, tel_id_filter_list, event_id_filter_list, output_directory)


if __name__ == "__main__":
    main()


