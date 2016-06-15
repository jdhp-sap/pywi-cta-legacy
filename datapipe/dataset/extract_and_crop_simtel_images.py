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
...
"""

__all__ = ['crop']

import argparse
import numpy as np

def crop(img):
    """
    ...
    """

    # Telescopes "ASTRI"

    img_map = np.zeros([8*5, 8*5], dtype=int)

    img_map[0*8:1*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 29 * 64
    img_map[0*8:1*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 30 * 64
    img_map[0*8:1*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 31 * 64
    img_map[0*8:1*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 32 * 64
    img_map[0*8:1*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 33 * 64

    img_map[1*8:2*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 23 * 64
    img_map[1*8:2*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 24 * 64
    img_map[1*8:2*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 25 * 64
    img_map[1*8:2*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 26 * 64
    img_map[1*8:2*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 27 * 64

    img_map[2*8:3*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 16 * 64
    img_map[2*8:3*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 17 * 64
    img_map[2*8:3*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 18 * 64
    img_map[2*8:3*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 19 * 64
    img_map[2*8:3*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 20 * 64

    img_map[3*8:4*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  9 * 64
    img_map[3*8:4*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 10 * 64
    img_map[3*8:4*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 11 * 64
    img_map[3*8:4*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 12 * 64
    img_map[3*8:4*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 13 * 64

    img_map[4*8:5*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  3 * 64
    img_map[4*8:5*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  4 * 64
    img_map[4*8:5*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  5 * 64
    img_map[4*8:5*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  6 * 64
    img_map[4*8:5*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  7 * 64

    #print(img_map)

    cropped_img = img[[img_map.ravel()]].reshape([8*5, 8*5])

    return cropped_img

def main():

    # PARSE OPTIONS ###########################################################

#    parser = argparse.ArgumentParser(description="...")
#
#    parser.add_argument("fileargs", nargs=1, metavar="FILE",
#                        help="The file image to process (FITS or PNG)")
#    args = parser.parse_args()
#
#    input_file_path = args.fileargs[0]

    ###########################################################################

    img = np.arange(2368)
    cropped_img = crop(img)

    print("cropped image", cropped_img)


if __name__ == "__main__":
    main()

