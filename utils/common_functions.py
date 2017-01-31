#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import copy

import json
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors
#import matplotlib.ticker
from matplotlib.patches import Ellipse
from matplotlib.colors import LogNorm

import math

import astropy.units as u
from ctapipe.image.hillas import hillas_parameters_1 as hillas_parameters_1
from ctapipe.image.hillas import hillas_parameters_2 as hillas_parameters_2

COLOR_MAP = "gray_r" # "gnuplot2" # "gray"


# DIRECTORY PARSER ############################################################

def get_fits_files_list(directory_path):
    """
    Return the list of all FITS file's path in `directory_path`.
    """

    # Parse the input directory
    print("Parsing", directory_path)

    fits_file_name_list = [os.path.join(directory_path, file_name)
                           for file_name
                           in os.listdir(directory_path)
                           if os.path.isfile(os.path.join(directory_path, file_name))
                           and file_name.endswith((".fits", ".fit"))]

    return fits_file_name_list


# JSON PARSER #################################################################

def parse_json_file(json_file_path):
    with open(json_file_path, "r") as fd:
        json_data = json.load(fd)
    return json_data


# FILTERS (RETURN A SUBSET OF JSON_DICT) ######################################

def image_filter_equals(json_dict, key, value):
    """Return a version of `json_dict` where only `io` list items (images) with
    `key`==`velue` are kept."""

    json_dict["io"] = [image_dict for image_dict in json_dict["io"] if image_dict[key]==value]

    return json_dict


def image_filter_range(json_dict, key, min_value, max_value):
    """Return a version of `json_dict` where only `io` list items (images) with
    `key`'s value in range `[min_velue ; max_value]` are kept."""

    json_dict["io"] = [image_dict for image_dict in json_dict["io"] if min_value <= image_dict[key] <= max_value]

    return json_dict


# JSON TO 1D OR 2D ARRAYS #####################################################

def extract_score_array(json_dict, metric):

    if isinstance(metric, int):
        score_array = _extract_score_array_index(json_dict, metric)
    elif isinstance(metric, str):
        score_array = _extract_score_array_name(json_dict, metric)
    else:
        raise TypeError("Wrong type")

    return score_array


def _extract_score_array_index(json_dict, score_index):
    io_list = json_dict["io"]
    score_list = [image_dict["score"][score_index] for image_dict in io_list if "score" in image_dict]
    score_array = np.array(score_list)
    return score_array


def _extract_score_array_name(json_dict, metric):
    io_list = json_dict["io"]

    score_list = []
    for image_dict in io_list:
        if "score" in image_dict and "score_name" in image_dict:
            score = [pair[1] for pair in zip(image_dict["score_name"], image_dict["score"]) if pair[0] == metric]   # TODO: a bit dirty...
            if len(score) != 1:
                raise Exception("{} has {} occurrences in the score list (should have exactly one occurrence)".format(metric, len(score)))
            score_list.append(score[0])

    score_array = np.array(score_list)
    return score_array


def extract_score_2d_array(json_dict, score_index1, score_index2):
    io_list = json_dict["io"]
    score_list = [(image_dict["score"][score_index1], image_dict["score"][score_index2]) for image_dict in io_list if "score" in image_dict]
    score_2d_array = np.array(score_list)
    return score_2d_array


def extract_metadata_array(json_dict, key):
    io_list = json_dict["io"]

    metadata_list = [image_dict[key] for image_dict in io_list if "score" in image_dict]
    metadata_array = np.array(metadata_list)

    return metadata_array


def extract_metadata_2d_array(json_dict, key1, key2, exclude_aborted=False, aborted_only=False):
    io_list = json_dict["io"]

    if exclude_aborted:
        metadata_list = [(image_dict[key1], image_dict[key2]) for image_dict in io_list if "error" not in image_dict]
    elif aborted_only:
        metadata_list = [(image_dict[key1], image_dict[key2]) for image_dict in io_list if "error" in image_dict]
    else:
        metadata_list = [(image_dict[key1], image_dict[key2]) for image_dict in io_list]

    metadata_2d_array = np.array(metadata_list)

    return metadata_2d_array

###############################################################################

def extract_min(data_list):
    """Extract the min value from a nested list.

    The following simpler version can't work because nested list can have
    different lenght:

    ``min_value = np.array(data_list).min()``

    Parameters
    ----------
    data_list : list
        A list of ndarray from wich the minimum value is extracted

    Returns
    -------
    float
        The minimum value of `data_list`
    """
    #min_value = np.ravel(data_list).min()

    min_value_array = np.array([np.ravel(data).min() for data in data_list])
    min_value = min_value_array.min()

    return min_value


def extract_max(data_list):
    """Extract the max value from a nested list.

    The following simpler version can't work because nested list can have
    different lenght:

    ``max_value = np.array(data_list).max()``

    Parameters
    ----------
    data_list : list
        A list of ndarray from wich the maximum value is extracted

    Returns
    -------
    float
        The maximum value of `data_list`
    """
    #max_value = np.ravel(data_list).max()

    max_value_array = np.array([np.ravel(data).max() for data in data_list])
    max_value = max_value_array.max()

    return max_value


# PLOT FUNCTIONS ##############################################################

def plot_image_meter(axis, image_array, pixels_position, title, plot_log_scale=False):

    axis.axis('equal')

    # See http://matplotlib.org/examples/pylab_examples/pcolor_demo.html

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

    hillas = hillas_parameters_2(xx.flatten(), # * u.meter,  # TODO
                                 yy.flatten(), # * u.meter,  # TODO
                                 image_array.flatten())

    centroid = (hillas.cen_x, hillas.cen_y)
    length = hillas.length
    width = hillas.width
    angle = hillas.psi.to(u.rad).value

    #print("centroid:", centroid)
    #print("length:",   length)
    #print("width:",    width)
    #print("angle:",    angle)

    ellipse = Ellipse(xy=centroid, width=length, height=width, angle=np.degrees(angle), fill=False, color='red', lw=2)
    axis.axes.add_patch(ellipse)

    title = axis.axes.get_title()
    axis.axes.set_title("{} ({:.2f}°)".format(title, np.degrees(angle)))

    # Plot the center of the ellipse

    axis.scatter(*centroid, c="r", marker="x", linewidth=2)

    # Plot the shower axis

    p0_x = centroid[0]
    p0_y = centroid[1]

    p1_x = p0_x + math.cos(angle)
    p1_y = p0_y + math.sin(angle)

    p2_x = p0_x + math.cos(angle + math.pi) 
    p2_y = p0_y + math.sin(angle + math.pi) 

    axis.plot([p1_x, p2_x], [p1_y, p2_y], ':r', lw=2)

    p3_x = p0_x + math.cos(angle) * length / 2.
    p3_y = p0_y + math.sin(angle) * length / 2.

    axis.plot([p0_x, p3_x], [p0_y, p3_y], '-r')

    p4_x = p0_x + math.cos(angle + math.pi/2.) * width / 2.
    p4_y = p0_y + math.sin(angle + math.pi/2.) * width / 2.

    axis.plot([p0_x, p4_x], [p0_y, p4_y], '-g')

    # Set (back) axis limits

    pos_x_min, pos_x_max = pixels_position[0].min(), pixels_position[0].max()
    pos_y_min, pos_y_max = pixels_position[1].min(), pixels_position[1].max()

    axis.set_xlim(xmin=pos_x_min)
    axis.set_xlim(xmax=pos_x_max)
    axis.set_ylim(ymin=pos_y_min)
    axis.set_ylim(ymax=pos_y_max)


def plot_correlation(axis, x_array, y_array, x_label, y_label, logx=False, logy=False):
    """
    data_array must have the following shape: (2, N)
    """

    axis.plot(x_array, y_array, '.', alpha=0.2)

    # Info box
    axis.text(0.95, 0.92,
            "{} images".format(x_array.shape[0]),
            verticalalignment = 'top',
            horizontalalignment = 'right',
            transform = axis.transAxes,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})


    axis.set_xlabel(x_label, fontsize=20)
    axis.set_ylabel(y_label, fontsize=20)

    plt.setp(axis.get_xticklabels(), fontsize=14)
    plt.setp(axis.get_yticklabels(), fontsize=14)

    if logx:
        axis.set_xscale("log")               # Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    if logy:
        axis.set_yscale("log")               # Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))


def plot_hist1d(axis,
                data_list,
                label_list=[],
                logx=False,
                logy=False,
                xmin=None,
                xmax=None,
                overlaid=False,
                hist_type='bar',
                alpha=0.5,
                xlabel=None,
                title_fontsize=20,
                xylabel_fontsize=20,
                xy_ticklabel_fontsize=14,
                legend_fontsize=16,
                title=None,
                linear_xlabel_style=None,   # 'sci'
                linear_ylabel_style='sci',
                num_bins=None,
                tight=False,
                show_info_box=True,
                info_box_x_location=0.03,
                info_box_y_location=0.95,
                info_box_num_samples=True,
                info_box_mean=True,
                info_box_rms=True,
                info_box_std=False,
                verbose=False):
    """
    Fill a matplotlib axis with a 1 dimension histogram.

    data_list should be a list (or a tuple) of numpy arrays.
    """

    label_list = copy.deepcopy(label_list)

    if not isinstance(data_list, (list, tuple)):
        raise ValueError("Wrong data type: {} (list or tuple expected)".format(str(type(data_list))))

    if not isinstance(label_list, (list, tuple)):
        raise ValueError("Wrong data type: {} (list or tuple expected)".format(str(type(label_list))))

    if len(label_list) > 0 and (len(label_list) != len(data_list)):
        raise ValueError("Inconsistent data: len(label_list)={}, len(data_list)={}".format(str(len(label_list)), str(len(data_list))))

    # Simulate info box when len(data_list) > 0
    if len(label_list) > 1 and show_info_box:
        for index, (data_array, label) in enumerate(zip(data_list, label_list)):
            if info_box_num_samples:
                num_samples = data_array.shape[0]
                label += " num={:n}".format(num_samples)

            if info_box_mean:
                mean = data_array.mean()
                label += r" $\bar{x}$=" + "{:.3g}".format(mean)

            if info_box_rms:
                rms = np.sqrt(np.mean(np.square(data_array)))
                label += " rms={:e}".format(rms)

            if info_box_std:
                std = data_array.std()
                label += r" $\sigma$=" + "{:.3g}".format(std)

            label_list[index] = label

    if logx:
        # Setup the logarithmic scale on the X axis
        vmin = np.log10(extract_min(data_list))
        vmax = np.log10(extract_max(data_list))
        bins = np.logspace(vmin, vmax, num_bins if num_bins is not None else 50) # Make a range from 10**vmin to 10**vmax
    elif num_bins is not None:
        #bins = np.linspace(extract_min(data_list), extract_max(data_list) + 1, num_bins + 1)
        bins = num_bins
    else:
        # bins=[0, 1, 2, 3] make the following bins: [0,1[, [1,2[ and [2,3]
        # For more information, see:
        # - https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
        # - http://stackoverflow.com/questions/15177203/how-is-the-pyplot-histogram-bins-interpreted
        bins = list(range(math.floor(extract_min(data_list)), math.floor(extract_max(data_list)) + 2))

    if overlaid:
        for data_array, label in zip(data_list, label_list):
            res_tuple = axis.hist(data_array,
                                  #bins=bins,
                                  log=logy,           # Set log scale on the Y axis
                                  histtype=hist_type,
                                  alpha=alpha,
                                  label=label)
    else:
        res_tuple = axis.hist(data_list,
                              bins=bins,
                              log=logy,               # Set log scale on the Y axis
                              histtype=hist_type,
                              alpha=alpha,
                              label=label_list)

    if verbose:
        print(bins)
        print(res_tuple)

    # Legend
    axis.legend(prop={'size': legend_fontsize})

    # Labels
    axis.set_ylabel("Count", fontsize=xylabel_fontsize)
    if xlabel is not None:
        axis.set_xlabel(xlabel, fontsize=xylabel_fontsize)

    # Title
    if title is not None:
        axis.set_title(title, fontsize=title_fontsize)

    # Tick labels size
    plt.setp(axis.get_xticklabels(), fontsize=xy_ticklabel_fontsize)
    plt.setp(axis.get_yticklabels(), fontsize=xy_ticklabel_fontsize)

    # xmin and xmax
    if tight:
        if logx:
            xmin = np.log10(extract_min(data_list))
            xmax = np.log10(extract_max(data_list))
        else:
            xmin = extract_min(data_list)
            xmax = extract_max(data_list)

    if xmin is not None:
        axis.set_xlim(xmin=xmin)

    if xmax is not None:
        axis.set_xlim(xmax=xmax)

    if logy:
        axis.set_ylim(ymin=0.1)
    else:
        axis.set_ylim(ymin=0)

    # Log scale and tick label format
    if logx:
        axis.set_xscale("log")               # Activate log scale on X axis
    elif linear_xlabel_style == 'sci':
        axis.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    if (not logy) and (linear_ylabel_style == 'sci'):
        axis.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Info box
    if show_info_box and (len(data_list) == 1):
        info_list = []

        if info_box_num_samples:
            num_samples = data_list[0].shape[0]
            info_list.append("Num samples: {:n}".format(num_samples))

        if info_box_mean:
            mean = data_list[0].mean()
            info_list.append("Mean: {:g}".format(mean))

        if info_box_rms:
            rms = np.sqrt(np.mean(np.square(data_list[0])))
            #info_list.append("RMS: {:g}".format(rms))

        if info_box_std:
            std = data_list[0].std()
            info_list.append("STD: {:g}".format(std))

        axis.text(info_box_x_location, info_box_y_location,
                  "\n".join(info_list),
                  verticalalignment = 'top',
                  horizontalalignment = 'left',
                  transform = axis.transAxes,
                  bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

    return res_tuple


def plot_hist2d(axis,
                x_array,
                y_array,
                x_label,
                y_label,
                logx=False,
                logy=False,
                logz=False,
                xmin=None,
                xmax=None,
                ymin=None,
                ymax=None,
                zmin=None,
                zmax=None):

    if xmin is None:
        xmin = x_array.min()

    if xmax is None:
        xmax = x_array.max()

    if ymin is None:
        ymin = y_array.min()

    if ymax is None:
        ymax = y_array.max()

    print("xmin:", xmin)
    print("xmax:", xmax)
    print("ymin:", ymin)
    print("ymax:", ymax)


    # Log scale
    if logx:
        # Setup the logarithmic scale on the X axis
        logxmin = np.log10(xmin)
        logxmax = np.log10(xmax)
        xbins = np.logspace(logxmin, logxmax, 50) # <- make a range from 10**xmin to 10**xmax
    else:
        xbins = np.linspace(xmin, xmax, 50) # <- make a range from xmin to xmax

    if logy:
        logymin = np.log10(ymin)
        logymax = np.log10(ymax)
        ybins = np.logspace(logymin, logymax, 50) # <- make a range from 10**ymin to 10**ymax
    else:
        ybins = np.linspace(ymin, ymax, 50) # <- make a range from ymin to ymax

    # Plot
    counts, _, _ = np.histogram2d(x_array, y_array, bins=(xbins, ybins))

    counts = counts.T   # TODO CHECK THAT !!!!!!!!!!!!!!!!!!!!!!!!!!!!


    # zmin / zmax
    if zmin is None:
        zmin = counts.min()

    if zmax is None:
        zmax = counts.max()

    print("zmin:", zmin)
    print("zmax:", zmax)


    # Colorbar

    if logz:
    #    ## Setup the logarithmic scale on the Z axis
    #    #counts = np.log10(counts)

        pcm = axis.pcolormesh(xbins, ybins, counts, cmap='OrRd', norm=matplotlib.colors.SymLogNorm(linthresh=1., linscale=1., vmin=zmin, vmax=zmax))

    #    #MIN = .1
    #    #counts[counts == 0] = MIN
    #    #pcm = axis.pcolormesh(xbins, ybins, counts, cmap='OrRd', norm=matplotlib.colors.LogNorm(vmin=MIN, vmax=zmax))
    else:
        pcm = axis.pcolormesh(xbins, ybins, counts, vmin=zmin, vmax=zmax, cmap='OrRd')

    #formatter = matplotlib.ticker.LogFormatter(10, labelOnlyBase=False)
    #plt.colorbar(pcm, ax=axis, ticks=[1,5,10,20,50], format=formatter)

    plt.colorbar(pcm, ax=axis)


    # Log scale on axis
    if logx:
        axis.set_xscale("log")               # <- Activate log scale on X axis
    else:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    if logy:
        axis.set_yscale("log")               # <- Activate log scale on Y axis
    else:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Tight plot
    axis.set_xlim(xmin=xbins[0])
    axis.set_xlim(xmax=xbins[-1])
    axis.set_ylim(ymin=ybins[0])
    axis.set_ylim(ymax=ybins[-1])


    axis.set_xlabel(x_label, fontsize=16)
    axis.set_ylabel(y_label, fontsize=16)

    plt.setp(axis.get_xticklabels(), fontsize=14)
    plt.setp(axis.get_yticklabels(), fontsize=14)


# PERPENDICULAR HIT DISTRIBUTION ##############################################


def angle_and_point_to_line_equation(angle_radian, point):
    """
    point: a point the line goes through
    angle: the angle of the line (in radian)
    """

    a = math.tan(angle_radian)
    b = -1
    c = -math.tan(angle_radian) * point[0] + point[1]

    return a, b, c


def signed_distance_point_to_line(a, b, c, p):
    """
    Distance between a point p and a line defined by a, b and c.

    a, b, c: the line $x + by + c = 0$
    p: the point
    """
    d1 = (a*p[0] + b*p[1] + c)
    d2 = math.sqrt(math.pow(a, 2.) + math.pow(b, 2.))
    #d = abs(d1)/d2
    d = d1/d2
    return d


def orthogonal_projection_point_to_line(a, b, c, p):
    """
    Return the projection of the point p on the line defined by a, b and c with $x + by + c = 0$.
    """
    p2 = ((b*(b*p[0] - a*p[1]) - a*c)/(math.pow(a,2.)+math.pow(b,2.)),
          (a*(-b*p[0] + a*p[1]) - b*c)/(math.pow(a,2.)+math.pow(b,2.)))
    return p2


def perpendicular_hit_distribution(image_array, pixels_position):

    image_array = copy.deepcopy(image_array)
    pixels_position = copy.deepcopy(pixels_position)

    ###

    xx, yy = pixels_position[0], pixels_position[1]

    hillas = hillas_parameters_1(xx.flatten() * u.meter,
                                 yy.flatten() * u.meter,
                                 image_array.flatten())

    centroid = (hillas.cen_x.value, hillas.cen_y.value)
    length = hillas.length.value
    width = hillas.width.value
    angle = hillas.psi.to(u.rad).value

    #print("centroid:", centroid)
    #print("length:",   length)
    #print("width:",    width)
    #print("angle:",    angle)

    a, b, c = angle_and_point_to_line_equation(angle, centroid)

    #print("a:", a)
    #print("b:", b)
    #print("c:", c)

    ###

    pixel_stat_list = []

    for pixel_value, pixel_pos_x, pixel_pos_y in zip(image_array.flatten(),
                                                     pixels_position[0].flatten(),
                                                     pixels_position[1].flatten()):
        if pixel_value > 0:
            signed_distance = signed_distance_point_to_line(a, b, c, (pixel_pos_x, pixel_pos_y))
            projected_point = orthogonal_projection_point_to_line(a, b, c, (pixel_pos_x, pixel_pos_y))

            #print(pixel_pos_x, pixel_pos_y, pixel_value, signed_distance, *projected_point)

            pixel_stat_list.append([pixel_pos_x, pixel_pos_y, pixel_value, signed_distance, *projected_point])

    pixel_stat_array = np.array(pixel_stat_list)

    return pixel_stat_array


def plot_perpendicular_hit_distribution(axis,
                                        image_array_list,
                                        pixels_position,
                                        bins=None,
                                        label_list=None,
                                        hist_type='bar'):

    pixel_stat_array_list = []
    hist_list = []

    if label_list is None:
        label_list = [None] * len(image_array_list)

    for image_array, label in zip(image_array_list, label_list):
        pixel_stat_array = perpendicular_hit_distribution(image_array, pixels_position)

        if bins is None:
            hist = axis.hist(pixel_stat_array[:,3],
                             weights=pixel_stat_array[:,2],
                             bins=30,         # TODO
                             label=label,
                             histtype=hist_type,
                             alpha=0.5)
        else:
            hist = axis.hist(pixel_stat_array[:,3],
                             weights=pixel_stat_array[:,2],
                             bins=bins,         # TODO
                             label=label,
                             histtype=hist_type,
                             alpha=0.5)

        pixel_stat_array_list.append(pixel_stat_array)
        hist_list.append(hist)

    if label_list is not None:
        axis.legend(prop={'size': 14}) #, loc='lower center')

    return pixel_stat_array_list, hist_list


###############################################################################


def test_hist1d():
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    ## Check the (solved) bug occuring on the last bin when bins = integer list
    #data = np.array([1, 1, 1,
    #                 2, 2, 2,
    #                 3, 3, 3])
    #data = np.array([1, 1, 1,
    #                 2, 2, 2,
    #                 3.1, 3.1, 3.1])
    #data = np.array([1.1, 1.1, 1.1,
    #                 2, 2, 2,
    #                 3, 3, 3])
    #data = np.array([0.5, 0.5, 0.5,
    #                 1.5, 1.5, 1.5,
    #                 2.5, 2.5, 2.5])

    #hist = plot_hist1d(ax1, [data], logy=True)


    ## Check the (solved) bug on invisible bins when bin values = 1 and y scale is log
    #data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #                 2,
    #                 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])

    #hist = plot_hist1d(ax1, [data], logy=True)


    ## Check with linscale
    #data = np.array([1, 1, 1,
    #                 2, 2, 2,
    #                 3, 3, 3])
    #data = np.array([1, 1, 1,
    #                 2, 2, 2,
    #                 3.1, 3.1, 3.1])
    #data = np.array([1.1, 1.1, 1.1,
    #                 2, 2, 2,
    #                 3, 3, 3])
    #data = np.array([0.5, 0.5, 0.5,
    #                 1.5, 1.5, 1.5,
    #                 2.5, 2.5, 2.5])

    #hist = plot_hist1d(ax1, [data], num_bins=3)

    print(hist)
    plt.show()

if __name__ == '__main__':
    test_hist1d()

