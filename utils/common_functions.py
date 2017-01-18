#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import json
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors
#import matplotlib.ticker

import math


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
    min_value = np.ravel(data_list).min()
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
    max_value = np.ravel(data_list).max()
    return max_value

# PLOT FUNCTIONS ##############################################################

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
                label_list,
                logx=False,
                logy=False,
                xmin=None,
                xmax=None,
                overlaid=False,
                hist_type='bar',
                alpha=0.5,
                xlabel=None,
                xylabel_fontsize=20,
                title=None,
                linear_xlabel_style='sci',
                linear_ylabel_style='sci',
                num_bins=None,
                show_info_box=True,
                info_box_x_location=0.03,
                info_box_y_location=0.95,
                info_box_num_samples=True,
                info_box_mean=True,
                info_box_rms=True,
                info_box_std=False):
    """
    Fill a matplotlib axis with a 1 dimension histogram.

    data_list should be a list (or a tuple) of numpy arrays.
    """

    if not isinstance(data_list, (list, tuple)):
        raise ValueError("Wrong data type: {} (list or tuple expected)".format(str(type(data_list))))

    if not isinstance(label_list, (list, tuple)):
        raise ValueError("Wrong data type: {} (list or tuple expected)".format(str(type(label_list))))

    if len(label_list) > 0 and (len(label_list) != len(data_list)):
        raise ValueError("Inconsistent data: len(label_list)={}, len(data_list)={}".format(str(len(label_list)), str(len(data_list))))

    # Simulate info box when len(data_list) > 0
    if len(label_list) > 0 and show_info_box:
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
        bins = np.linspace(extract_min(data_list), extract_max(data_list), num_bins)
    else:
        bins = range(math.floor(extract_min(data_list)), math.ceil(extract_max(data_list)))

    if overlaid:
        for data_array, label in zip(data_list, label_list):
            res_tuple = axis.hist(data_array,
                                  bins=bins,
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

    axis.legend(prop={'size': 20})

    axis.set_ylabel("Count", fontsize=xylabel_fontsize)
    if xlabel is not None:
        axis.set_xlabel(xlabel, fontsize=xylabel_fontsize)

    if title is not None:
        axis.set_title(title, fontsize=20)

    plt.setp(axis.get_xticklabels(), fontsize=14)
    plt.setp(axis.get_yticklabels(), fontsize=14)

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


def plot_hist2d(axis, x_array, y_array, x_label, y_label, logx=False, logy=False, logz=False, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):

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

