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
Plot a FITS file.

Example usages:
  ./utils/plot_image.py -h
  ./utils/plot_image.py ./test.fits
  ipython3 -- ./utils/plot_image.py ./test.fits
"""

import common_functions as common

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import LogNorm

import copy
import math

from datapipe.io import images

import astropy.units as u
from ctapipe.image.hillas import hillas_parameters_1 as hillas_parameters_1
from ctapipe.image.hillas import hillas_parameters_2 as hillas_parameters_2

COLOR_MAP = "gray_r" # "gnuplot2" # "gray"

##############################################

def plot_image_meter(axis, image_array, pixels_position, title, plot_log_scale=False):

    axis.axis('equal')

    # See http://matplotlib.org/examples/pylab_examples/pcolor_demo.html

    print(pixels_position)
    print(pixels_position.shape)

    # generate 2 2d grids for the x & y bounds
    x, y = pixels_position[0], pixels_position[1]

    z_min, z_max = image_array.min(), image_array.max()

    if plot_log_scale:
        # See http://matplotlib.org/examples/pylab_examples/pcolor_log.html
        #     http://stackoverflow.com/questions/2546475/how-can-i-draw-a-log-normalized-imshow-plot-with-a-colorbar-representing-the-raw
        im = axis.pcolor(x, y, image_array, norm=LogNorm(vmin=0.01, vmax=image_array.max()), cmap=COLOR_MAP)  # TODO: "vmin=0.01" is an arbitrary choice...
    else:
        im = axis.pcolor(x, y, image_array, cmap=COLOR_MAP, vmin=z_min, vmax=z_max)

    plt.colorbar(im, ax=axis) # draw the colorbar

    axis.set_title(title)


def plot_ellipse_shower_on_image_meter(axis, image_array, pixels_position):

    xx, yy = pixels_position[0], pixels_position[1]

    hillas = hillas_parameters_2(xx.flatten(), # * u.meter,
                                 yy.flatten(), # * u.meter,
                                 image_array.flatten())

    centroid = (hillas.cen_x, hillas.cen_y)
    length = hillas.length
    width = hillas.width
    angle = hillas.psi.to(u.rad).value # - np.pi/2.   # TODO

    print("centroid:", centroid)
    print("length:",   length)
    print("width:",    width)
    print("angle:",    angle)

    #print("DEBUG:", hillas[7].value, angle, np.degrees(angle))

    #ellipse = Ellipse(xy=centroid, width=length, height=width, angle=np.degrees(angle), fill=False, color='red', lw=2)   # TODO
    ellipse = Ellipse(xy=centroid, width=length, height=width, angle=np.degrees(angle), fill=False, color='red', lw=2)
    axis.axes.add_patch(ellipse)

    title = axis.axes.get_title()
    axis.axes.set_title("{} ({:.2f}°)".format(title, np.degrees(angle)))

    # Plot centroid

    axis.scatter(*centroid)

    # Plot shower axis

    #axis.arrow(0, 0,  0.1, 0, head_width=0.001, head_length=0.005, fc='k', ec='k')
    #axis.arrow(0, 0,  0, 0.1, head_width=0.001, head_length=0.005, fc='k', ec='k')

    p1_x = centroid[0]
    p1_y = centroid[1]

    p2_x = p1_x + math.cos(angle)
    p2_y = p1_y + math.sin(angle)
    #p2_x = p1_x + (length / 2.) * math.cos(angle)
    #p2_y = p1_y + (length / 2.) * math.sin(angle)


    #print(math.cos(math.pi/2.))
    #print(math.sin(math.pi/2.))
    #p2_x = p1_x + (length / 2.) * math.cos(math.pi/2.)
    #p2_y = p1_y + (length / 2.) * math.sin(math.pi/2.)
    #print(p1_x, p2_x)
    #print(p1_y, p2_x)


    axis.arrow(p1_x, p1_y,  p2_x, p2_y, head_width=0.001, head_length=0.005, fc='r', ec='r')

    p3_x = p1_x + math.cos(angle + math.pi/2.)
    p3_y = p1_y + math.sin(angle + math.pi/2.)
    #p3_x = p1_x + (width / 2.) * math.cos(angle + math.pi/2.)
    #p3_y = p1_y + (width / 2.) * math.sin(angle + math.pi/2.)

    axis.arrow(p1_x, p1_y, p3_x, p3_y, head_width=0.001, head_length=0.005, fc='g', ec='g')

    # Plot origin axis

    #axis.arrow(p1_x, p1_y, p1_x + 1, p1_y, head_width=0.001, head_length=0.005, fc='r', ec='r')
    #axis.arrow(p1_x, p1_y, p1_x, p1_y + 1, head_width=0.001, head_length=0.005, fc='g', ec='g')

    #ellipse = Ellipse(xy=centroid, width=0.2, height=0.05, angle=0, fill=False, color='black', lw=2)
    #axis.axes.add_patch(ellipse)




def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Plot a FITS file.")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None, metavar="FILE",
                        help="The output file path (image file)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The files image to process (FITS).")

    args = parser.parse_args()

    quiet = args.quiet
    output = args.output
    input_file_path = args.fileargs[0]

    # READ THE INPUT FILE #####################################################

    fits_images_dict, fits_metadata_dict = images.load_benchmark_images(input_file_path)

    reference_img = fits_images_dict["reference_image"]
    pixels_position = fits_images_dict["pixels_position"]

    # ASSESS OR PRINT THE CLEANED IMAGE #######################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(9, 9))

    plot_image_meter(ax1, reference_img, pixels_position, "Reference image")
    plot_ellipse_shower_on_image_meter(ax1, reference_img, pixels_position)

    # PLOT AND SAVE ###########################################################

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    if output is None:
        output = "{}.png".format(base_file_path)

    plt.savefig(output, bbox_inches='tight')

    if not quiet:
        plt.show()


if __name__ == "__main__":
    main()

