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

__all__ = ['normalize_array',
           'metric1',
           'metric2',
           'metric3',
           'metric4',
           'metric5',
           'metric6',
           'assess_image_cleaning']

import numpy as np
from astropy.units import Quantity
import astropy.units as u

from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_psnr as psnr
from skimage.measure import compare_nrmse as nrmse


###############################################################################
# EXCEPTIONS                                                                  #
###############################################################################

class AssessError(Exception):
    pass

class UnknownMethod(AssessError):
    pass

class EmptyOutputImageError(AssessError):
    """
    Exception raised when the output image only have null pixels (to prevent
    division by 0 in the assess function).
    """

    def __init__(self):
        super(EmptyOutputImageError, self).__init__("Empty output image error")

class EmptyReferenceImageError(AssessError):
    """
    Exception raised when the reference image only have null pixels (to prevent
    division by 0 in the assess function).
    """

    def __init__(self):
        super(EmptyReferenceImageError, self).__init__("Empty reference image error")


###############################################################################
# TOOL FUNCTIONS                                                              #
###############################################################################

def normalize_array(input_array):
    r"""Normalize the given image such that its pixels value fit between 0.0
    and 1.0.

    It applies

    .. math::

        \text{normalize}(\boldsymbol{s}) = \frac{ \boldsymbol{s} - \text{min}(\boldsymbol{s}) }{ \text{max}(\boldsymbol{s}) - \text{min}(\boldsymbol{s}) }

    where :math:`\boldsymbol{s}` is the input array (an image).

    Parameters
    ----------
    image : Numpy array
        The image to normalize (whatever its shape)

    Returns
    -------
    Numpy array
        The normalized version of the input image (keeping the same dimension
        and shape)
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)

    output_array = (input_array - input_array.min()) / (input_array.max() - input_array.min())
    return output_array


###############################################################################
# METRIC FUNCTIONS                                                            #
###############################################################################

# Mean Pixel Difference with Normalization (mpd) ##############################

def metric1(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`.

    This function is **depreciated** as it is not adapted to high dynamic range
    images handled with this project.

    It applies

    .. math::

        f(\hat{\boldsymbol{s}}, \boldsymbol{s}^*) = \text{mean} \left( \text{abs} \left( \text{normalize}(\hat{\boldsymbol{s}}) - \text{normalize}(\boldsymbol{s}^*) \right) \right)

    if `normalize_images = True`,
    otherwise it applies

    .. math::

        f(\hat{\boldsymbol{s}}, \boldsymbol{s}^*) = \text{mean} \left( \text{abs} \left( \hat{\boldsymbol{s}} - \boldsymbol{s}^* \right) \right)

    with :math:`\hat{\boldsymbol{s}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{s}^*` the reference image
    (i.e. the *clean* image).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    if (params is not None) and ('normalize_images' in params) and (params['normalize_images']):
        normalized_diff_array = normalize_array(output_image) - normalize_array(reference_image)
        mark = np.mean(np.abs(normalized_diff_array))
    else:
        diff_array = output_image - reference_image
        mark = np.mean(np.abs(diff_array))

    return mark


# Mean Pixel Difference 2 #####################################################

def metric2(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the :math:`\mathcal{E}_{\text{shape}}` metric.

    It applies

    .. math::

        f(\hat{\boldsymbol{s}}, \boldsymbol{s}^*) = \text{mean} \left( \text{abs} \left( \frac{\hat{\boldsymbol{s}}}{\sum_i \hat{\boldsymbol{s}}_i} - \frac{\boldsymbol{s}^*}{\sum_i \boldsymbol{s}^*_i} \right) \right)

    with :math:`\hat{\boldsymbol{s}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{s}^*` the reference image
    (i.e. the *clean* image).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if sum_output_image <= 0:                 # TODO
        raise EmptyOutputImageError()

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = np.mean(np.abs((output_image / sum_output_image) - (reference_image / sum_reference_image)))

    return mark


# Relative Total Counts Difference (mpdspd) ###################################

def metric3(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the :math:`\mathcal{E}^+_{\text{energy}}`
    (a.k.a. *relative total counts difference*) metric.

    It applies

    .. math::

        f(\hat{\boldsymbol{s}}, \boldsymbol{s}^*) = \frac{ \text{abs} \left( \sum_i \hat{\boldsymbol{s}}_i - \sum_i \boldsymbol{s}^*_i \right) }{ \sum_i \boldsymbol{s}^*_i }

    with :math:`\hat{\boldsymbol{s}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{s}^*` the reference image
    (i.e. the *clean* image).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = np.abs(sum_output_image - sum_reference_image) / sum_reference_image

    return mark


# Signed Relative Total Counts Difference (sspd) ##############################

def metric4(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the :math:`\mathcal{E}_{\text{energy}}`
    (a.k.a. *signed relative total counts difference*) metric.
    
    It applies

    .. math::

        f(\hat{\boldsymbol{s}}, \boldsymbol{s}^*) = \frac{ \sum_i \hat{\boldsymbol{s}}_i - \sum_i \boldsymbol{s}^*_i }{ \sum_i \boldsymbol{s}^*_i }

    with :math:`\hat{\boldsymbol{s}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{s}^*` the reference image
    (i.e. the *clean* image).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.sum(output_image))
    sum_reference_image = float(np.sum(reference_image))

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = (sum_output_image - sum_reference_image) / sum_reference_image

    return mark


# Structural Similarity Index Measure (SSIM) ##################################

def metric5(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the *Structural Similarity Index Measure* (SSIM) metric.

    See [1]_, [2]_, [3]_ and [4]_ for more information.
    
    The SSIM index is calculated on various windows of an image.
    The measure between two windows :math:`x` and :math:`y` of common size
    :math:`N.N` is:

    .. math::
        \hbox{SSIM}(x,y) = \frac{(2\mu_x\mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 + c_2)}

    with:

    * :math:`\scriptstyle\mu_x` the average of :math:`\scriptstyle x`;
    * :math:`\scriptstyle\mu_y` the average of :math:`\scriptstyle y`;
    * :math:`\scriptstyle\sigma_x^2` the variance of :math:`\scriptstyle x`;
    * :math:`\scriptstyle\sigma_y^2` the variance of :math:`\scriptstyle y`;
    * :math:`\scriptstyle \sigma_{xy}` the covariance of :math:`\scriptstyle x` and :math:`\scriptstyle y`;
    * :math:`\scriptstyle c_1 = (k_1L)^2`, :math:`\scriptstyle c_2 = (k_2L)^2` two variables to stabilize the division with weak denominator;
    * :math:`\scriptstyle L` the dynamic range of the pixel-values (typically this is :math:`\scriptstyle 2^{\#bits\ per\ pixel}-1`);
    * :math:`\scriptstyle k_1 = 0.01` and :math:`\scriptstyle k_2 = 0.03` by default.

    The SSIM index satisfies the condition of symmetry:

    .. math::

        \text{SSIM}(x, y) = \text{SSIM}(y, x)

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.

    References
    ----------
    .. [1] Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P.
       (2004). Image quality assessment: From error visibility to
       structural similarity. IEEE Transactions on Image Processing,
       13, 600-612.
       https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf,
       DOI:10.1.1.11.2477
    .. [2] Avanaki, A. N. (2009). Exact global histogram specification
       optimized for structural similarity. Optical Review, 16, 613-621.
       http://arxiv.org/abs/0901.0065,
       DOI:10.1007/s10043-009-0119-z
    .. [3] http://scikit-image.org/docs/dev/api/skimage.measure.html#compare-ssim
    .. [4] https://en.wikipedia.org/wiki/Structural_similarity
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)

    ssim_val, ssim_image = ssim(output_image, reference_image, full=True, gaussian_weights=True, sigma=0.5)

    return ssim_val


# Peak Signal-to-Noise Ratio (PSNR) ###########################################

def metric6(input_img, output_image, reference_image, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the *Peak Signal-to-Noise Ratio* (PSNR) metric.

    See [5]_ and [6]_ for more information.
    
    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.

    References
    ----------
    .. [5] http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.compare_psnr
    .. [6] https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)

    psnr_val = psnr(output_image, reference_image, dynamic_range=1e3)

    return psnr_val


###############################################################################
# ASSESS FUNCTIONS DRIVER                                                     #
###############################################################################

BENCHMARK_DICT = {
    "mpd":      (metric1,),
    "e_shape":  (metric2,),
    "e_energy": (metric3,),
    "mpdspd":   (metric2, metric3),
    "sspd":     (metric4,),
    "ssim":     (metric5,),
    "psnr":     (metric6,),
    "all":      (metric2, metric3, metric4, metric5)
}

METRIC_NAME_DICT = {
    metric1: "mpd",
    metric2: "e_shape",
    metric3: "e_energy",
    metric4: "sspd",
    metric5: "ssim",
    metric6: "psnr"
}

def assess_image_cleaning(input_img, output_img, reference_img, benchmark_method, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the `benchmark_method` metrics:

    - "mpd":      (metric1)
    - "e_shape":  (metric2)
    - "e_energy": (metric3)
    - "mpdspd":   (metric2, metric3)
    - "sspd":     (metric4)
    - "ssim":     (metric5)
    - "psnr":     (metric6)
    - "all":      (metric2, metric3, metric4, metric5, metric6)

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_img: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_img: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).

    Returns
    -------
    tuple of float numbers
        The score(s) of the image cleaning algorithm for the given image.
    """

    try:
        score_list = [metric_function(input_img, output_img, reference_img, params) for metric_function in BENCHMARK_DICT[benchmark_method]]
        metric_name_list = [METRIC_NAME_DICT[metric_function] for metric_function in BENCHMARK_DICT[benchmark_method]]
    except KeyError:
        raise UnknownMethod()

    return tuple(score_list), tuple(metric_name_list)

