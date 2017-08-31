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

PACKAGE_PATH = os.path.split(__file__)[0]

ASTRI_GEOM_FILE = os.path.join(PACKAGE_PATH,         'astri.geom.json')
ASTRI_CROPPED_GEOM_FILE = os.path.join(PACKAGE_PATH, 'astri_cropped.geom.json')
FLASHCAM_GEOM_FILE = os.path.join(PACKAGE_PATH,      'flashcam2d.geom.json')
GCT_GEOM_FILE = os.path.join(PACKAGE_PATH,           'gct.geom.json')
LSTCAM_GEOM_FILE = os.path.join(PACKAGE_PATH,        'lstcam2d.geom.json')
NECTARCAM_GEOM_FILE = os.path.join(PACKAGE_PATH,     'nectarcam2d.geom.json')

__all__ = ['ASTRI_GEOM_FILE',
           'ASTRI_CROPPED_GEOM_FILE',
           'FLASHCAM_GEOM_FILE',
           'GCT_GEOM_FILE',
           'LSTCAM_GEOM_FILE',
           'NECTARCAM_GEOM_FILE']
