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

from ctapipe.utils import linalg

import astropy.units as u
from ctapipe.image.hillas import hillas_parameters_1 as hillas_parameters_1
from ctapipe.image.hillas import hillas_parameters_2 as hillas_parameters_2


COLOR_MAP = "gray_r" # "gnuplot2" # "gray"


def rotation_matrix_2d(angle_rad):
    """construct a 2D rotation matrix as a numpy NDArray that rotates a
    vector clockwise. Angle should be any object that can be converted
    into an `astropy.coordinates.Angle`
    """
    return np.array([[np.cos(angle_rad), -np.sin(angle_rad)], [np.sin(angle_rad), np.cos(angle_rad)]])


def rotate(pixels_position, angle_rad):
    """rotate the camera coordinates about the center of the camera by
    specified angle.

    Taken from ctapipe.io.camera.rotate()
    """
    pix_x, pix_y = pixels_position[0], pixels_position[1]

    rotmat = rotation_matrix_2d(angle_rad)

    print(rotmat)
    print(pix_x[0])
    print(pix_y[:,0])

    pix_x = pix_x[0]
    pix_y = pix_y[:,0]

    rotated = np.dot(rotmat.T, [pix_x, pix_y])
    pix_x = rotated[0]
    pix_y = rotated[1]

    return np.array(np.meshgrid(pix_x, pix_y))


##############################################


def plot_image_meter(axis, image_array, pixels_position, title, plot_log_scale=False):

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


###############################################################################


def plot_image(axis, image_array, title, plot_log_scale=False):

    #im = axis.imshow(image_array,
    #                 origin='lower',
    #                 interpolation='nearest',
    #                 vmin=min(image_array.min(), 0),
    #                 cmap=COLOR_MAP)

    # See http://matplotlib.org/examples/pylab_examples/pcolor_demo.html

    dx, dy = 1, 1

    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, image_array.shape[0], dy), slice(0, image_array.shape[1], dx)]  # TODO !!!

    z_min, z_max = image_array.min(), image_array.max()

    if plot_log_scale:
        # See http://matplotlib.org/examples/pylab_examples/pcolor_log.html
        #     http://stackoverflow.com/questions/2546475/how-can-i-draw-a-log-normalized-imshow-plot-with-a-colorbar-representing-the-raw
        im = axis.pcolor(x, y, image_array, norm=LogNorm(vmin=0.01, vmax=image_array.max()), cmap=COLOR_MAP)  # TODO: "vmin=0.01" is an arbitrary choice...
    else:
        im = axis.pcolor(x, y, image_array, cmap=COLOR_MAP, vmin=z_min, vmax=z_max)

    plt.colorbar(im, ax=axis) # draw the colorbar

    axis.set_title(title)


def plot_ellipse_shower_on_image(axis, image_array):
    """Based on Fabio's notebook."""

    x = np.arange(0, np.shape(image_array)[0], 1)
    y = np.arange(0, np.shape(image_array)[1], 1)
    xx, yy = np.meshgrid(x, y)

    hillas = hillas_parameters_2(xx.flatten(), # * u.meter,
                                 yy.flatten(), # * u.meter,
                                 image_array.flatten())

    centroid = (hillas.cen_x.value, hillas.cen_y.value)
    length = hillas.length.value
    width = hillas.width.value
    angle = hillas.psi.to(u.rad).value # - np.pi/2.    # TODO

    print("centroid:", centroid)
    print("length:",   length)
    print("width:",    width)
    print("angle:",    angle)

    #print("DEBUG:", hillas[7].value, angle, np.degrees(angle))

    ellipse = Ellipse(xy=centroid, width=width, height=length, angle=np.degrees(angle), fill=False, color='red', lw=2)
    axis.axes.add_patch(ellipse)

    title = axis.axes.get_title()
    axis.axes.set_title("{} ({:.2f}°)".format(title, np.degrees(angle)))

    # Plot centroid

    axis.scatter(*centroid)

    # Plot shower axis

    ellipse = Ellipse(xy=centroid, width=width, height=0, angle=np.degrees(angle), fill=False, color='blue', lw=2)
    axis.axes.add_patch(ellipse)

    ellipse = Ellipse(xy=centroid, width=0, height=length, angle=np.degrees(angle), fill=False, color='blue', lw=2)
    axis.axes.add_patch(ellipse)

    # Plot origin axis

    ellipse = Ellipse(xy=centroid, width=10, height=0, angle=0, fill=False, color='black', lw=2)
    axis.axes.add_patch(ellipse)


#def plot_perpendicular_hit_distribution_jd(histogram_axis, image_axis, image_array, pixels_position, title):
#
#    image_array = copy.deepcopy(image_array)
#
#    print(image_array)
#    print(image_array.shape)
#
#    print(pixels_position)
#    print(pixels_position.shape)
#
#    # p1 = center of the ellipse
#    #p1_x = hillas.cen_x
#    #p1_y = hillas.cen_y


def plot_perpendicular_hit_distribution(histogram_axis, image_axis, image_array, pixels_position, title):

    image_array = copy.deepcopy(image_array)

    ###

    #size_m = 0.2  # Size of the "phase space" in meter
    size_m = 0.2  # Size of the "phase space" in meter

#     # TODO: clean these following hard coded values for Astri
#    num_pixels_x = 40
#    num_pixels_y = 40
#
#    x = np.linspace(-0.142555996776, 0.142555996776, num_pixels_x)
#    y = np.linspace(-0.142555996776, 0.142555996776, num_pixels_y)
#
#    #x = np.arange(0, np.shape(ref_image_array)[0], 1)          # TODO: wrong values -10 10 21
#    #y = np.arange(0, np.shape(ref_image_array)[1], 1)          # TODO: wrong values  (30, ...)
#
#    xx, yy = np.meshgrid(x, y)
#    print("delta x:", xx - pixels_position[0])
#    print("delta y:", yy - pixels_position[1])

    xx, yy = pixels_position[0], pixels_position[1]

    # Based on Tino's evaluate_cleaning.py (l. 277)
    hillas = hillas_parameters_1(xx.flatten() * u.meter,      # TODO: essayer avec hillas param 2 !!!
                                 yy.flatten() * u.meter,
                                 image_array.flatten())       # [0]

    centroid = (hillas.cen_x, hillas.cen_y)
    length = hillas.length
    width = hillas.width
    angle = np.radians(hillas.psi) # - np.pi/2.   # TODO

    print("centroid:", centroid)
    print("length:",   length)
    print("width:",    width)
    print("angle:",    angle)

    ###

    # p1 = center of the ellipse
    p1_x = hillas.cen_x
    p1_y = hillas.cen_y

    #image_axis.scatter(p1_x, p1_y)  # DEBUG plot

    # p2 = intersection between the ellipse and the shower track
    p2_x = p1_x + hillas.length * np.cos(angle)  # hillas.psi + np.pi/2)
    p2_y = p1_y + hillas.length * np.sin(angle)  # hillas.psi + np.pi/2)

    #image_axis.scatter(p2_x, p2_y)               # DEBUG plot
    #image_axis.plot([p1_x, p2_x], [p1_y, p2_y])  # DEBUG plot

    print(p1_x, p2_x, p1_y, p2_y)                # DEBUG plot

    d12_x = p1_x - p2_x
    d12_y = p1_y - p2_y

    print(d12_x, d12_y)                # DEBUG plot

    # Slope of the shower track
    T = linalg.normalise(np.array([d12_x.value, d12_y.value]))  # why a dedicated function ? if it's what I understand, it can easily be done on the fly

    #print("[p1_x-p2_x, p1_y-p2_y]:", [p1_x-p2_x, p1_y-p2_y])
    #print("T:", T)
    #image_axis.plot([p1_x, p1_x*T[0]], [p1_y, p1_y*T[1]], "-g", linewidth=3)  # DEBUG plot

    x = xx.flatten()
    y = yy.flatten()

    # Manhattan distance of pixels to the center of the ellipse
    # Translate (center) on P1 ?
    D = [p1_x.value-x, p1_y.value-y]

    # Pixels in the new base
    dl = D[0]*T[0] + D[1]*T[1]
    dp = D[0]*T[1] - D[1]*T[0]

    # nparray.ravel(): Return a flattened array.
    values, bins, patches = histogram_axis.hist(dp.ravel(),
                                                histtype='step',
                                                bins=np.linspace(-size_m, size_m, 31))          # -10 10 21

    # TODO: scatter seulement  les points qui sont dans le linspace de bins defini juste au dessus, faire apparaitre chaque bin d'une couleure différente
    
    ##image_axis.scatter(dl, dp, s=10, alpha=0.5)               # DEBUG plot
    #image_axis.scatter(dl, dp, s=10, alpha=0.5)               # DEBUG plot
    #image_axis.plot(dl.reshape(40, 40).T, dp.reshape(40, 40).T)               # DEBUG plot
    #print(dl)
    #print(dp.shape)

    ###

    histogram_axis.set_xlim([-size_m, size_m])

    histogram_axis.set_xlabel('Distance to the shower axis (m)', fontsize=14)
    histogram_axis.set_ylabel('Hits', fontsize=14)

    histogram_axis.set_title(title)


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


    ## MAKE MOCK DATA ##################

    #mean = [0, 0]
    #cov = [[.0305, .09],
    #       [.01, .0305]]
    #
    #x, y = np.random.multivariate_normal(mean, cov, 50000).T

    ##counts, _, _ = np.histogram2d(x, y, bins=(xbins, ybins))
    #counts, _, _ = np.histogram2d(x, y, bins=40)
    ##counts = counts.T   # TODO check that

    #counts[counts < 100] = 0

    #reference_img1 = counts

    #reference_img1[0, 0] = 1

    ## MAKE MOCK DATA ##################

    #mean = [0, 0]
    #cov = [[.05, .09],
    #       [.01, .05]]
    #
    #x, y = np.random.multivariate_normal(mean, cov, 50000).T

    ##counts, _, _ = np.histogram2d(x, y, bins=(xbins, ybins))
    #counts, _, _ = np.histogram2d(x, y, bins=40)
    ##counts = counts.T   # TODO check that

    #counts[counts < 100] = 0

    #reference_img2 = counts
    #reference_img2[0, 0] = 1

    ####################################

    #bw_reference_img1 = np.copy(reference_img1)
    #bw_reference_img1[reference_img1 > 0] = 1   # simplify the image (black and white image)


    #bw_reference_img2 = np.copy(reference_img2)
    #bw_reference_img2[reference_img2 > 0] = 1   # simplify the image (black and white image)

    ###################################


    #pixels_position = rotate(pixels_position, math.pi)


    # ASSESS OR PRINT THE CLEANED IMAGE #######################################

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(16, 9))

    ##plot_image(ax1, reference_img1, "Reference image")
    ##plot_ellipse_shower_on_image(ax1, reference_img1)

    #plot_image_meter(ax2, bw_reference_img1, pixels_position, "Reference image")
    #plot_ellipse_shower_on_image_meter(ax2, reference_img1, pixels_position)

    #plot_perpendicular_hit_distribution(ax3, ax2, bw_reference_img1, pixels_position, "Perpendicular hit distribution JD")



    ##plot_image(ax4, reference_img2, "Reference image")
    ##plot_ellipse_shower_on_image(ax4, reference_img2)

    #plot_image_meter(ax5, bw_reference_img2, pixels_position, "Reference image")
    #plot_ellipse_shower_on_image_meter(ax5, reference_img2, pixels_position)

    #plot_perpendicular_hit_distribution(ax6, ax5, bw_reference_img2, pixels_position, "Perpendicular hit distribution JD")


    plot_image_meter(ax2, reference_img, pixels_position, "Reference image")
    plot_ellipse_shower_on_image_meter(ax2, reference_img, pixels_position)

    plot_perpendicular_hit_distribution(ax3, ax2, reference_img, pixels_position, "Perpendicular hit distribution JD")


    plot_image_meter(ax5, reference_img, pixels_position, "Reference image")
    plot_ellipse_shower_on_image_meter(ax5, reference_img, pixels_position)

    plot_perpendicular_hit_distribution(ax6, ax5, reference_img, pixels_position, "Perpendicular hit distribution JD")




    #plot_image(ax4, bw_reference_img1, "Reference image")
    #plot_ellipse_shower_on_image(ax4, bw_reference_img1)

    #plot_image_meter(ax5, bw_reference_img1, pixels_position, "Reference image")

    #plot_perpendicular_hit_distribution(ax6, ax5, bw_reference_img1, pixels_position, "Perpendicular hit distribution")



    #a = np.array([[0, 1,],
    #              [0, 2]])
    #print(a)
    #print(rotate(a, -math.pi))
    

    # PLOT AND SAVE ###########################################################

    base_file_path = os.path.basename(input_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    if output is None:
        output = "{}.pdf".format(base_file_path)

    plt.savefig(output, bbox_inches='tight')

    if not quiet:
        plt.show()


if __name__ == "__main__":
    main()

