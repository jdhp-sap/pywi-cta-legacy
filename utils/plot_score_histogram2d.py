#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
#import math
import os

import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.ticker

import numpy as np

# histtype : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HIST_TYPE='bar'
ALPHA=0.5


def parse_json_file(json_file_path):
    with open(json_file_path, "r") as fd:
        json_data = json.load(fd)
    return json_data


def extract_score_array(json_dict, score_index):
    io_list = json_dict["io"]
    score_list = [image_dict["score"][score_index] for image_dict in io_list if "score" in image_dict]
    score_array = np.array(score_list)
    return score_array


def extract_metadata_array(json_dict, key):
    io_list = json_dict["io"]
    metadata_list = [image_dict[key] for image_dict in io_list if "score" in image_dict]
    metadata_array = np.array(metadata_list)
    return metadata_array


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


def plot_hist2d(axis, x_array, y_array, logx=False, logy=False, logz=False, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):
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


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("--key", "-k", required=True, metavar="STRING",
                        help='The key of the value to plot (e.g. "mc_energy" or "npe")')

    parser.add_argument("--logx", action="store_true", default=False,
                        help="Use a logaritmic scale on the X axis")

    parser.add_argument("--logy", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--logz", action="store_true", default=False,
                        help="Use a logaritmic scale on the Y axis")

    parser.add_argument("--index", "-i", type=int, default=0, metavar="INT", 
                        help="The index of the score to plot in case of multivalued scores")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--title", default=None,
                        metavar="STRING",
                        help="The title of the plot")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()

    key = args.key
    logx = args.logx
    logy = args.logy
    logz = args.logz
    score_index = args.index
    title = args.title
    quiet = args.quiet
    json_file_path_list = args.fileargs

    if args.output is None:
        output_file_path = "scores2d_i{}.pdf".format(score_index)
    else:
        output_file_path = args.output

    # FETCH SCORE #############################################################

    score_array_list = []
    metadata_array_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        json_dict = parse_json_file(json_file_path)

        score_array = extract_score_array(json_dict, score_index)
        score_array_list.append(score_array)

        metadata_array = extract_metadata_array(json_dict, key)
        metadata_array_list.append(metadata_array)

        label_list.append(json_dict["label"])

    xmin = extract_min(score_array_list)
    xmax = extract_max(score_array_list)
    ymin = extract_min(metadata_array_list)
    ymax = extract_max(metadata_array_list)

    # PLOT STATISTICS #########################################################

    fig, axis_array = plt.subplots(nrows=1, ncols=len(json_file_path_list), squeeze=False, figsize=(6 * len(json_file_path_list), 6))

    axis_array = axis_array.flat

    for (axis, score_array, metadata_array, label) in zip(axis_array, score_array_list, metadata_array_list, label_list):

        plot_hist2d(axis, score_array, metadata_array, logx, logy, logz, xmin, xmax, ymin, ymax, zmin=None, zmax=None)

        axis.legend(prop={'size': 20})

        # Sub titles
        axis.set_title(label, fontsize=20)

        axis.set_xlabel("score", fontsize=20)
        axis.set_ylabel(key, fontsize=20)

        plt.setp(axis.get_xticklabels(), fontsize=14)
        plt.setp(axis.get_yticklabels(), fontsize=14)


    # Main title
    if title is not None:
        fig.suptitle(title, fontsize=20)
    else:
        suffix = " (index {})".format(score_index)
        fig.suptitle("Score" + suffix, fontsize=20)

    plt.subplots_adjust(top=0.85)

    # Save file and plot ########

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()

