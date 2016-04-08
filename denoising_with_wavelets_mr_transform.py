#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script originally came from https://github.com/jdhp-sap/snippets/tree/master/mr_transform

import argparse
from astropy.io import fits

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

"""
This script makes image denoising with mr_transform (a tool written by the
CosmoStat group to compute wavelets transforms on images).
"""


def get_image_array_from_fits_file(file_path):
    
    hdu_list = fits.open(file_path)   # open the FITS file

    if len(hdu_list) != 1:
        raise Exception("The FITS file should contain only one HDU.")

    image_array = hdu_list[0].data    # "hdu.data" is a Numpy Array

    hdu_list.close()

    return image_array


def save_image(img, output_file_path, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.savefig(output_file_path)
    plt.close('all')


def plot_image(img, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.show()


def main():

    # PARSE OPTIONS ###############################################################

    parser = argparse.ArgumentParser(description="MrTransform wrapper.")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")
    parser.add_argument("filearg", nargs=1, metavar="FILE",
                        help="the FITS file to process")

    args = parser.parse_args()

    number_of_scales = args.number_of_scales
    input_file_path = args.filearg[0]

    base_file_path = os.path.splitext(input_file_path)[0]
    output_file_path = base_file_path + "_mr_planes.fits"


    # READ THE INPUT FILE #########################################################

    input_img = get_image_array_from_fits_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # EXECUTE MR_TRANSFORM ########################################################

    # TODO: improve the following lines
    cmd = 'mr_transform -n{} "{}" out'.format(number_of_scales, input_file_path)
    os.system(cmd)

    # TODO: improve the following lines
    cmd = "mv out.mr {}".format(output_file_path)
    os.system(cmd)


    # READ THE MR_TRANSFORM OUTPUT FILE ###########################################

    output_imgs = get_image_array_from_fits_file(output_file_path)

    if output_imgs.ndim != 3:
        raise Exception("Unexpected error: the output FITS file should contain a 3D array.")


    # DENOISE THE INPUT IMAGE WITH MR_TRANSFORM PLANES ############################

    denoised_img = np.zeros(input_img.shape)

    for img_index, img in enumerate(output_imgs):

        if img_index < (len(output_imgs) - 1):  # All planes except the last one

            # Compute the standard deviation of the plane ###########

            img_sigma = np.std(img)

            # Apply a threshold on the plane ########################

            # Remark: "abs(img) > (img_sigma * 3.)" should be the correct way to
            # make the image mask, but sometimes results looks better when all
            # negative coefficients are dropped ("img > (img_sigma * 3.)")

            #img_mask = abs(img) > (img_sigma * 3.)  
            img_mask = img > (img_sigma * 3.)
            filtered_img = img * img_mask

            #save_image(img,
            #           "{}_plane{}.png".format(base_file_path, img_index),
            #           title="Plane {}".format(img_index))
            #save_image(img_mask,
            #           "{}_plane{}_mask.png".format(base_file_path, img_index),
            #           title="Binary mask for plane {}".format(img_index))
            #save_image(filtered_img,
            #           "{}_plane{}_filtered.png".format(base_file_path, img_index),
            #           title="Filtered plane {}".format(img_index))

            #plot_image(img, title="Plane {}".format(img_index))
            #plot_image(img_mask, title="Binary mask for plane {}".format(img_index))
            #plot_image(filtered_img, title="Filtered plane {}".format(img_index))

            # Sum the plane #########################################

            denoised_img = denoised_img + filtered_img

        else:   # The last plane should be kept unmodified

            #save_image(img,
            #           "{}_plane{}.png".format(base_file_path, img_index),
            #           title="Plane {}".format(img_index))
            #plot_image(img, title="Plane {}".format(img_index))

            # Sum the last plane ####################################

            denoised_img = denoised_img + img

    #save_image(input_img,
    #           "{}.png".format(base_file_path),
    #           title="Original image")
    #save_image(denoised_img,
    #           "{}_denoised.png".format(base_file_path),
    #           title="Filtered image")

    plot_image(input_img, title="Original image")
    plot_image(denoised_img, title="Filtered image")


if __name__ == "__main__":
    main()

