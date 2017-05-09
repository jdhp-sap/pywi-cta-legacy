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

__all__ = ['simtel_to_geom_json_file']

import argparse
import numpy as np

import ctapipe
from ctapipe.io.hessio import hessio_event_source
import pyhessio

from datapipe.io import geometry_converter

# Old version
from ctapipe.io import camera

# New version
#from ctapipe.instrument import camera

from datapipe import __version__ as VERSION


def simtel_to_geom_json_file(simtel_file_path, tel_id, output_json_file=None):

    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_id])

    for ev in source:
        event = ev

    # Get the geometry object with the "guess()" method

    pix_x = event.inst.pixel_pos[tel_id][0]
    pix_y = event.inst.pixel_pos[tel_id][1]
    optical_foclen = event.inst.optical_foclen[tel_id]

    geom = camera.CameraGeometry.guess(pix_x, pix_y, optical_foclen)

    # Convert and write the geom object

    if output_json_file is None:
        output_json_file = geom.cam_id.lower() + ".geom.json"

    geometry_converter.geom_to_json_file(geom, output_json_file)


def main():

    # PARSE OPTIONS ###########################################################

    desc = "Generate geom.json file form simtel a file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t",
                        type=int,
                        default=1,
                        metavar="INTEGER",
                        help="The telescopes to query (default: 1)")

    parser.add_argument("--output", "-o",
                        metavar="FILE",
                        help="The geom.json output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_id = args.telescope
    output_file = args.output
    simtel_file_path = args.fileargs[0]

    simtel_to_geom_json_file(simtel_file_path, tel_id, output_file)


if __name__ == "__main__":
    main()

