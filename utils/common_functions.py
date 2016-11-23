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


def parse_json_file(json_file_path):
    with open(json_file_path, "r") as fd:
        json_data = json.load(fd)
    return json_data

###############################################################################

def extract_score_array(json_dict, score_index):
    io_list = json_dict["io"]
    score_list = [image_dict["score"][score_index] for image_dict in io_list if "score" in image_dict]
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
    min_value = np.concatenate(data_list).min()
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
    max_value = np.concatenate(data_list).max()
    return max_value

###############################################################################

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


def plot_hist2d(axis, x_array, y_array, x_label, y_label, logx=False, logy=False, logz=False, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):
    """
    data_array must have the following shape: (2, N)
    """

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

