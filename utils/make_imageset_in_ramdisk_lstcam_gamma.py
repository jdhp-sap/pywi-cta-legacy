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

import os
import random
import shutil

from datapipe.io import images


NUM_IMAGES = 1000

INPUT_DIR_PATH = os.path.expanduser("~/data/grid_prod3b_north/fits/lst/gamma")
OUTPUT_FILE_PATH = "/dev/shm/.jd/lstcam/gamma"

NPE_MIN = 30
NPE_MAX = 2000


# TODO: filter contained images -> pb: la meth doit etre adaptee pour les images hexagonales...

# MAKE THE FILE LIST ##########################################################

assert os.path.isdir(OUTPUT_FILE_PATH)

print(INPUT_DIR_PATH)

input_file_path_list = []

for dir_item in os.listdir(INPUT_DIR_PATH):
    dir_item_path = os.path.join(INPUT_DIR_PATH, dir_item)
    if dir_item_path.lower().endswith('.fits') and os.path.isfile(dir_item_path):
        input_file_path_list.append(dir_item_path)

print("The input directory contains {} FITS files.".format(len(input_file_path_list)))

# SHUFFLE THE FILE LIST #######################################################

# shuffle the list to avoid having always the same tel_id
random.shuffle(input_file_path_list)

# COPY FILES IN THE RAMDISK ###################################################

image_counter = 0

for input_file_path in input_file_path_list:

    if image_counter > NUM_IMAGES:
        break

    fits_images_dict, fits_metadata_dict = images.load_benchmark_images(input_file_path)

    if NPE_MIN <= fits_metadata_dict["npe"] <= NPE_MAX:
        print(image_counter, input_file_path)
        shutil.copy(input_file_path, OUTPUT_FILE_PATH)
        image_counter += 1
    else:
        print("reject", input_file_path)

