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
But: construire une distribution à partir d'un modèle empirique ("inverse transform sampling").

Implémentation en Python:
* http://www.astroml.org/book_figures/chapter3/fig_clone_distribution.html
* https://github.com/astroML/astroML/blob/master/astroML/density_estimation/empirical.py
* https://github.com/astroML/astroML/blob/0287fe00c429b28b3ddf52435a32543f43246349/astroML/density_estimation/tests/test_empirical.py
* http://www.astroml.org/modules/generated/astroML.density_estimation.EmpiricalDistribution.html#astroML.density_estimation.EmpiricalDistribution
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.splprep.html
* https://docs.scipy.org/doc/scipy/reference/interpolate.html
* https://en.wikipedia.org/wiki/Inverse_transform_sampling


Mon implémentation:
* Ne pas garder tous les points comme ils le font dans astroml (j'ai plusieurs centaines de millions se samples...)
* A la place, utiliser np.histogram pour faire un CDF avec un nombre de bins choisi
* Stocker ce CDF dans un fichier
* Ecrire une classe pour générer des echantillons: charger et interpoller (avec des splines) le CDF dans __init__: interpolate.splrep(y, data)
* Fonction rvs qui génère un echantillon: interpolate.splev(y, self._tck)
"""

__all__ = ['EmpiricalDistribution']

# See the "simtel_signal_and_noise_histograms_plus_save_cdf_plus_test_inverse_transform_sampling" notebook

import numpy as np
import scipy.interpolate
import json

from . import cdf

INTERPOLATION_METH = 'spline1'

def get_cdf_file_path(cam_id):
    if cam_id == 'LSTCam':
        cdf_file_path = cdf.LSTCAM_CDF_FILE
    elif cam_id == 'NectarCam':
        cdf_file_path = cdf.NECTARCAM_CDF_FILE
    elif cam_id == 'FlashCam':
        cdf_file_path = cdf.FLASHCAM_CDF_FILE
    elif cam_id == 'DigiCam':
        cdf_file_path = cdf.DIGICAM_CDF_FILE
    elif cam_id == 'CHEC':
        cdf_file_path = cdf.GCT_CDF_FILE
    elif cam_id == 'ASTRICam':
        cdf_file_path = cdf.ASTRI_CDF_FILE
    else:
        raise NotImplementedError("Unknown camera {}.".format(cam_id))

    return cdf_file_path 


class EmpiricalDistribution:
    def __init__(self, cdf_json_file_path):
        with open(cdf_json_file_path, "r") as fd:
            cdf = json.load(fd)
            
        # Get the CDF

        self.cdf_x = np.array(cdf['cdf_x'])
        self.cdf_y = np.array(cdf['cdf_y'])

        # "Clean" data to have an actual inverse CDF (i.e. lets the CDF be *strictly* increasing)
        
        filtered_x_list = []
        filtered_y_list = []
        for i, (yip, yi) in enumerate(zip(self.cdf_y[0:-1], self.cdf_y[1:])):
            if yi > yip:
                filtered_x_list.append(self.cdf_x[i])
                filtered_y_list.append(self.cdf_y[i])

        filtered_x_array = np.array(filtered_x_list)
        filtered_y_array = np.array(filtered_y_list)
        
        # Interpolate CDF^{-1}

        if INTERPOLATION_METH == 'spline1':
            # Spline interpolation
            self.spl = scipy.interpolate.splrep(filtered_y_array, filtered_x_array,
                                                xb=0., xe=1.,   # The interval to fit
                                                #s=0.,          # A smoothing factor
                                                k=1)            # The degree fo the spline fit
        elif INTERPOLATION_METH == 'linear':
            # Linear interpolation with extrapolation
            self.inv_cdf = scipy.interpolate.interp1d(filtered_y_array, filtered_x_array,
                                                      kind='linear',
                                                      fill_value="extrapolate")
        elif INTERPOLATION_METH == 'slinear':
            # Spline linear interpolation with extrapolation (should be the same than spline1...)
            self.inv_cdf = scipy.interpolate.interp1d(filtered_y_array, filtered_x_array,
                                                      kind='slinear',
                                                      fill_value="extrapolate")
        else:
            raise Exception("Unknown interpolation method", INTERPOLATION_METH)

    def rvs(self, size):
        x = np.random.random(size)
        
        if INTERPOLATION_METH == 'spline1':
            return scipy.interpolate.splev(x, self.spl)
        elif INTERPOLATION_METH in ('linear', 'slinear'):
            return self.inv_cdf(x)
        else:
            raise Exception("Unknown interpolation method", INTERPOLATION_METH)

