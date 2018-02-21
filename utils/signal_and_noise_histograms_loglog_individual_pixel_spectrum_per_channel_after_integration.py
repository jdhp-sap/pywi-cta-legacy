#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Signal and noise histograms per channel

import numpy as np
import pandas as pd

import os
from os.path import expanduser

import datapipe
from datapipe.io import geometry_converter
from datapipe.io.images import image_generator
from datapipe.io.images import plot_ctapipe_image
from datapipe.io.images import plot_hillas_parameters_on_axes
from datapipe.io.images import print_hillas_parameters
from datapipe.io.images import hillas_parameters_to_df
from datapipe.image.hillas_parameters import get_hillas_parameters
from datapipe.denoising import wavelets_mrtransform
from datapipe.denoising.wavelets_mrtransform import WaveletTransform
from datapipe.denoising import inverse_transform_sampling
from datapipe.denoising.inverse_transform_sampling import EmpiricalDistribution

MAX_NUM_SAMPLES = 100000000 #0
PARTICLE = "gamma"   # "gamma" or "proton"

# Common functions ##############################

def get_samples(file_path_list,
                cam_id,
                max_num_samples):
    
    print("Cam ID:", cam_id)
    print("Input files:", file_path_list)

    df = pd.DataFrame(index=range(max_num_samples), columns=["channel0", "channel1"])
    
    # ITERATE OVER IMAGES #########################################

    index = 0
    for image in image_generator(file_path_list,
                                 cam_filter_list=[cam_id],
                                 ctapipe_format=True):
        
        #assert cam_id == image.meta['cam_id']
        
        # GET IMAGES ##########################################

        pe_image = image.input_image
        #assert pe_image.ndim == 2 and pe_image.shape[0] == 2, pe_image.shape

        # ADD SAMPLES #########################################

        index_end = index + pe_image[0].shape[0] - 1
        
        if index_end < max_num_samples:
            df.at[index:index_end, "channel0"] = pe_image[0]
            df.at[index:index_end, "channel1"] = pe_image[1]
        else:
            remaining = max_num_samples - index
            df.at[index:, "channel0"] = pe_image[0][0:remaining]
            df.at[index:, "channel1"] = pe_image[1][0:remaining]
            break
        
        index = index_end + 1
    
    # Save data (HDF5)
    file = "individual_pixel_spectra_channels_integrated_{}.h5".format(cam_id)
    df.to_hdf(file, key='df')
    
#################################################

if PARTICLE == "gamma":
    file_path = [expanduser("~/data/grid_prod3b_north/simtel/gamma/gamma_20deg_0deg_run103___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz")]
elif PARTICLE == "proton":
    file_path = [expanduser("~/data/grid_prod3b_north/simtel/proton/proton_20deg_0deg_run50001___cta-prod3-lapalma3-2147m-LaPalma.simtel.gz")]
else:
    raise ValueError("Wrong PARTICLE value: {}".format(PARTICLE))

# NectarCam - Grid Prod3b North

get_samples(file_path, cam_id="NectarCam", max_num_samples=MAX_NUM_SAMPLES)

# LSTcam - Grid Prod3b North

get_samples(file_path, cam_id="LSTCam", max_num_samples=MAX_NUM_SAMPLES)

