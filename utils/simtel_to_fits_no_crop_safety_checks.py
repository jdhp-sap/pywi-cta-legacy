#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm

from astropy.io import fits
import os.path

import datapipe
import common_functions as common


def plot(data, title="", log=False):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_title(title)
    
    if log:
        # See http://matplotlib.org/examples/pylab_examples/pcolor_log.html
        #     http://stackoverflow.com/questions/2546475/how-can-i-draw-a-log-normalized-imshow-plot-with-a-colorbar-representing-the-raw
        #im = ax1.pcolor(x, y, image_array, norm=LogNorm(vmin=0.01, vmax=image_array.max()), cmap=self.color_map)  # TODO: "vmin=0.01" is an arbitrary choice...
        im = ax1.imshow(data, interpolation='nearest', origin='lower', norm=LogNorm(vmin=0.01, vmax=data.max()), cmap="gnuplot2")   # cmap=cm.inferno and cmap="inferno" are both valid
    else:
        im = ax1.imshow(data, interpolation='nearest', origin='lower', cmap="gnuplot2")   # cmap=cm.inferno and cmap="inferno" are both valid
        #im = ax1.pcolor(x, y, image_array, cmap=self.color_map, vmin=z_min, vmax=z_max)

    plt.colorbar(im, ax=ax1)  # draw the colorbar
    
    plt.show()


def load_benchmark_images_deprecated(input_file_path):
    hdu_list = fits.open(input_file_path)   # open the FITS file

    if (len(hdu_list) != 6) or (not hdu_list[0].is_image) or (not hdu_list[1].is_image) or (not hdu_list[2].is_image) or (not hdu_list[3].is_image) or (not hdu_list[4].is_image) or (not hdu_list[5].is_image):
        hdu_list.close()
        raise WrongFitsFileStructure(input_file_path)

    hdu0, hdu1, hdu2, hdu3, hdu4, hdu6 = hdu_list

    # IMAGES

    images_dict = {}

    images_dict["input_image"] = hdu0.data        # "hdu.data" is a Numpy Array
    images_dict["reference_image"] = hdu1.data    # "hdu.data" is a Numpy Array
    images_dict["adc_sum_image"] = hdu2.data      # "hdu.data" is a Numpy Array
    images_dict["pedestal_image"] = hdu3.data     # "hdu.data" is a Numpy Array
    images_dict["gains_image"] = hdu4.data        # "hdu.data" is a Numpy Array
    #images_dict["calibration_image"] = hdu5.data # "hdu.data" is a Numpy Array
    images_dict["pixels_position"] = hdu6.data    # "hdu.data" is a Numpy Array

    # METADATA

    metadata_dict = {}
    hdu_list.close()

    return images_dict, metadata_dict


# SAFETY CHECK FOR GAMMAS #####################################################

path_not_cropped = "/Users/jdecock/data/astri_mini_array/fits/gamma/"
path_cropped = "/Users/jdecock/data/astri_mini_array/fits_cropped/gamma/"

cropped_file_path_list = common.get_fits_files_list(path_cropped)

for cropped_file_path in cropped_file_path_list:
    file_base = os.path.basename(cropped_file_path)
    #print(file_base)
    
    not_cropped_file_path = os.path.join(path_not_cropped, file_base)
    
    for key, cropped_data in load_benchmark_images_deprecated(cropped_file_path)[0].items():
        
        not_cropped_data = datapipe.io.images.load_benchmark_images(not_cropped_file_path)[0][key]
      
        if cropped_data.ndim == 2:
            test = np.all(not_cropped_data[8:6*8,8:6*8] == cropped_data)
            
            if not test:
                raise ValueError()
                
            #plot(cropped_data, title=key)
            #plot(not_cropped_data, title=key)
        elif cropped_data.ndim == 3:
            test1 = np.all(not_cropped_data[0][8:6*8,8:6*8] == cropped_data[0])
            test2 = np.all(not_cropped_data[1][8:6*8,8:6*8] == cropped_data[1])
            
            if not test1 and test2:
                raise ValueError()
                
            #plot(cropped_data[0], title=key + " [0]")
            #plot(not_cropped_data[0], title=key + " [0]")
            #plot(cropped_data[1], title=key + " [1]")
            #plot(not_cropped_data[1], title=key + " [1]")


# SAFETY CHECK FOR PROTONS ####################################################

path_not_cropped = "/Users/jdecock/data/astri_mini_array/fits/proton/"
path_cropped = "/Users/jdecock/data/astri_mini_array/fits_cropped/proton/"

cropped_file_path_list = common.get_fits_files_list(path_cropped)

for cropped_file_path in cropped_file_path_list:
    file_base = os.path.basename(cropped_file_path)
    #print(file_base)
    
    not_cropped_file_path = os.path.join(path_not_cropped, file_base)
    
    for key, cropped_data in load_benchmark_images_deprecated(cropped_file_path)[0].items():
        
        not_cropped_data = datapipe.io.images.load_benchmark_images(not_cropped_file_path)[0][key]
      
        if cropped_data.ndim == 2:
            test = np.all(not_cropped_data[8:6*8,8:6*8] == cropped_data)
            
            if not test:
                raise ValueError()
                
            #plot(cropped_data, title=key)
            #plot(not_cropped_data, title=key)
        elif cropped_data.ndim == 3:
            test1 = np.all(not_cropped_data[0][8:6*8,8:6*8] == cropped_data[0])
            test2 = np.all(not_cropped_data[1][8:6*8,8:6*8] == cropped_data[1])
            
            if not test1 and test2:
                raise ValueError()
                
            #plot(cropped_data[0], title=key + " [0]")
            #plot(not_cropped_data[0], title=key + " [0]")
            #plot(cropped_data[1], title=key + " [1]")
            #plot(not_cropped_data[1], title=key + " [1]")

