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
           'metric_mse',
           'metric_nrmse',
           'metric1',
           'metric2',
           'metric3',
           'metric4',
           'metric_ssim',
           'metric_psnr',
           'metric_delta_psi',
           'metric_hillas_delta',
           'metric_hillas_delta2',
           'metric_kill_isolated_pixels',
           'assess_image_cleaning']

import astropy.units as u

import collections

import numpy as np
import math

from datapipe.image.hillas_parameters import get_hillas_parameters

from datapipe.image.kill_isolated_pixels import kill_isolated_pixels
from datapipe.image.kill_isolated_pixels import kill_isolated_pixels_stats

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

        \text{normalize}(\boldsymbol{S}) = \frac{ \boldsymbol{S} - \text{min}(\boldsymbol{S}) }{ \text{max}(\boldsymbol{S}) - \text{min}(\boldsymbol{S}) }

    where :math:`\boldsymbol{S}` is the input array (an image).

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
    input_array = input_array.astype('float64', copy=True)

    min_value = np.nanmin(input_array)
    max_value = np.nanmax(input_array)

    output_array = (input_array - min_value) / float(max_value - min_value)

    return output_array


def norm_angle_diff(angle_in_degrees):
    """Normalize the difference of 2 angles in degree.

    This function is used to normalize the "delta psi" angle.
    """
    return abs(((angle_in_degrees + 90) % 180) - 90.)


###############################################################################
# METRIC FUNCTIONS                                                            #
###############################################################################

# Mean-Squared Error (MSE) ####################################################

def metric_mse(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the *Mean-Squared Error* (MSE) metric.

    It applies

    .. math::

        \text{MSE}(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \left\langle \left( \hat{\boldsymbol{S}} - \boldsymbol{S}^* \right)^{\circ 2} \right\rangle

    with:
    
    - :math:`\hat{\boldsymbol{S}}` the algorithm's output image (i.e. the
      *cleaned* image);
    - :math:`\boldsymbol{S}^*` the reference image (i.e. the *clean* image);
    - :math:`\langle \boldsymbol{S} \rangle` the average of matrix
      :math:`\boldsymbol{S}`;
    - :math:`\boldsymbol{S}^{\circ 2}` the
      `Hadamar power <https://en.wikipedia.org/wiki/Hadamard_product_(matrices)#Analogous_operations>`_
      (i.e. the element wise square) of matrix :math:`\boldsymbol{S}`.

    See http://scikit-image.org/docs/dev/api/skimage.measure.html#compare-mse
    for more information.

    Note
    ----
    This function is not well-suited to high dynamic range images handled with
    this project (errors are correlated with energy levels).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.

    
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    score = np.nanmean(np.square(output_image - reference_image))

    return float(score)


# Normalized Root Mean-Squared Error (NRMSE) ##################################

def metric_nrmse(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the *Normalized Root Mean-Squared Error* (NRMSE) metric.

    It applies

    .. math::

        \text{NRMSE}(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \frac{\sqrt{\text{MSE}}}{\sqrt{ \left\langle \hat{\boldsymbol{S}} \circ \boldsymbol{S}^* \right\rangle }}

    with:
    
    - :math:`\hat{\boldsymbol{S}}` the algorithm's output image (i.e. the
      *cleaned* image);
    - :math:`\boldsymbol{S}^*` the reference image (i.e. the *clean* image);
    - :math:`\langle \boldsymbol{S} \rangle` the average of matrix
      :math:`\boldsymbol{S}`;
    - :math:`\circ` the
      `Hadamar product <https://en.wikipedia.org/wiki/Hadamard_product_(matrices)>`_
      (i.e. the element wise product operator).

    See http://scikit-image.org/docs/dev/api/skimage.measure.html#compare-nrmse and
    https://en.wikipedia.org/wiki/Root-mean-square_deviation for more information.

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.

    
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    #if (params is not None) and ('nrmse_normalize_type' in params) and (params['nrmse_normalize_type'].lower() == 'euclidian'):
    #    denom = 
    # TODO: see https://github.com/scikit-image/scikit-image/blob/master/skimage/measure/simple_metrics.py#L82

    mse = metric_mse(input_img, output_image, reference_image, params)
    denom = np.sqrt(np.nanmean((reference_image * output_image), dtype=np.float64))
    score = np.sqrt(mse) / denom

    return float(score)


# Unusual Normalized Root Mean-Squared Error (uNRMSE) #########################

def metric1(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with a (unusually) normalized version of the *Root Mean-Squared Error*
    (RMSE) metric.

    It applies

    .. math::

        \text{uNRMSE}(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \left\langle \left( \left( \hat{\boldsymbol{S}}_n - \boldsymbol{S}^*_n \right)^{\circ 2} \right)^{\circ \frac{1}{2}} \right\rangle

    with:
    
    - :math:`\hat{\boldsymbol{S}}_n`
      the algorithm's normalized output image (i.e. the *cleaned* image),
      (using :func:`normalize_array`);
    - :math:`\boldsymbol{S}^*_n`
      the normalized reference image (i.e. the *clean* image)
      (using :func:`normalize_array`);
    - :math:`\langle \boldsymbol{S} \rangle` the average of matrix
      :math:`\boldsymbol{S}`;
    - :math:`\boldsymbol{S}^{\circ 2}` the
      `Hadamar power <https://en.wikipedia.org/wiki/Hadamard_product_(matrices)#Analogous_operations>`_
      (i.e. the element wise square) of matrix :math:`\boldsymbol{S}`.

    Note
    ----
    This function is not robust to noise on extreme values.

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.

    
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    output_image = normalize_array(output_image)
    reference_image = normalize_array(reference_image)

    score = np.nanmean(np.square(output_image - reference_image))

    return float(score)


# Mean Pixel Difference 2 #####################################################

def metric2(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the :math:`\mathcal{E}_{\text{shape}}` metric.

    It applies

    .. math::

        f(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \left\langle \text{abs} \left( \frac{\hat{\boldsymbol{S}}}{\sum_i \hat{\boldsymbol{S}}_i} - \frac{\boldsymbol{S}^*}{\sum_i \boldsymbol{S}^*_i} \right) \right\rangle

    with:
    
    - :math:`\hat{\boldsymbol{S}}` the algorithm's output image
      (i.e. the *cleaned* image);
    - :math:`\boldsymbol{S}^*` the reference image (i.e. the *clean* image);
    - :math:`\langle \boldsymbol{S} \rangle` the average of matrix
      :math:`\boldsymbol{S}`.

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.nansum(output_image))
    sum_reference_image = float(np.nansum(reference_image))

    if sum_output_image <= 0:                 # TODO
        raise EmptyOutputImageError()

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = np.nanmean(np.abs((output_image / sum_output_image) - (reference_image / sum_reference_image)))

    return float(mark)


# Relative Total Counts Difference (mpdspd) ###################################

def metric3(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the :math:`\mathcal{E}^+_{\text{energy}}`
    (a.k.a. *relative total counts difference*) metric.

    It applies

    .. math::

        f(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \frac{ \text{abs} \left( \sum_i \hat{\boldsymbol{S}}_i - \sum_i \boldsymbol{S}^*_i \right) }{ \sum_i \boldsymbol{S}^*_i }

    with :math:`\hat{\boldsymbol{S}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{S}^*` the reference image
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
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.nansum(output_image))
    sum_reference_image = float(np.nansum(reference_image))

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = np.abs(sum_output_image - sum_reference_image) / sum_reference_image

    return float(mark)


# Signed Relative Total Counts Difference (sspd) ##############################

def metric4(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the :math:`\mathcal{E}_{\text{energy}}`
    (a.k.a. *signed relative total counts difference*) metric.
    
    It applies

    .. math::

        f(\hat{\boldsymbol{S}}, \boldsymbol{S}^*) = \frac{ \sum_i \hat{\boldsymbol{S}}_i - \sum_i \boldsymbol{S}^*_i }{ \sum_i \boldsymbol{S}^*_i }

    with :math:`\hat{\boldsymbol{S}}` the algorithm's output image
    (i.e. the *cleaned* image)
    and :math:`\boldsymbol{S}^*` the reference image
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
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)
    
    sum_output_image = float(np.nansum(output_image))
    sum_reference_image = float(np.nansum(reference_image))

    if sum_reference_image <= 0:              # TODO
        raise EmptyReferenceImageError()

    mark = (sum_output_image - sum_reference_image) / sum_reference_image

    return float(mark)


# Structural Similarity Index Measure (SSIM) ##################################

def metric_ssim(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
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
    params: dict
        Additional options.

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

    # TODO: the following two lines may be wrong...
    output_image[np.isnan(output_image)] = 0
    reference_image[np.isnan(reference_image)] = 0

    ssim_val, ssim_image = ssim(output_image, reference_image, full=True, gaussian_weights=True, sigma=0.5)

    return float(ssim_val)


# Peak Signal-to-Noise Ratio (PSNR) ###########################################

def metric_psnr(input_img, output_image, reference_image, pixels_position=None, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
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
    params: dict
        Additional options.

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

    # TODO: the following two lines may be wrong...
    output_image[np.isnan(output_image)] = 0
    reference_image[np.isnan(reference_image)] = 0

    #psnr_val = psnr(output_image, reference_image, dynamic_range=1e3)
    psnr_val = psnr(output_image, reference_image, data_range=1e3)

    return float(psnr_val)


# Delta psi ###################################################################

def metric_delta_psi(input_img, output_image, reference_image, pixels_position, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the following relative *psi parameters* (relative difference of shower angle between the cleaned image and the reference image).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    float
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)

    if params is not None and "kill" in params and params["kill"]:
        # Remove isolated pixels on the reference image before assessment.
        reference_image = kill_isolated_pixels(reference_image, threshold=params["kill_threshold"])

    if params is not None and "hillas_implementation" in params and params["hillas_implementation"] in (1, 2):
        # Remove isolated pixels on the reference image before assessment.
        hillas_implementation = params["hillas_implementation"]
    else:
        hillas_implementation = 2

    output_image_parameters = get_hillas_parameters(output_image, hillas_implementation, pixels_position)
    reference_image_parameters = get_hillas_parameters(reference_image, hillas_implementation, pixels_position)

    # Psi (shower direction angle)
    output_image_parameter_psi_rad = output_image_parameters.psi.to(u.rad).value
    reference_image_parameter_psi_rad = reference_image_parameters.psi.to(u.rad).value
    delta_psi_rad = reference_image_parameter_psi_rad - output_image_parameter_psi_rad

    normalized_delta_psi_deg = norm_angle_diff(math.degrees(delta_psi_rad))

    return normalized_delta_psi_deg


# Hillas delta ################################################################

def metric_hillas_delta(input_img, output_image, reference_image, pixels_position, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the following relative *Hillas parameters*:

    * :math:`\Delta_{\text{size}}   = \text{reference_image}_{\text{size}}   - \text{output_image}_{\text{size_out}}`
    * :math:`\Delta_{\text{cen_x}}  = \text{reference_image}_{\text{cen_x}}  - \text{output_image}_{\text{cen_x_out}}`
    * :math:`\Delta_{\text{cen_y}}  = \text{reference_image}_{\text{cen_y}}  - \text{output_image}_{\text{cen_y_out}}`
    * :math:`\Delta_{\text{length}} = \text{reference_image}_{\text{length}} - \text{output_image}_{\text{length_out}}`
    * :math:`\Delta_{\text{width}}  = \text{reference_image}_{\text{width}}  - \text{output_image}_{\text{width_out}}`
    * :math:`\Delta_{\text{r}}      = \text{reference_image}_{\text{r}}      - \text{output_image}_{\text{r_out}}`
    * :math:`\Delta_{\text{phi}}    = \text{reference_image}_{\text{phi}}    - \text{output_image}_{\text{phi_out}}`
    * :math:`\Delta_{\text{psi}}    = \text{reference_image}_{\text{psi}}    - \text{output_image}_{\text{psi_out}}`
    * :math:`\Delta_{\text{miss}}   = \text{reference_image}_{\text{miss}}   - \text{output_image}_{\text{miss_out}}`

    See http://adsabs.harvard.edu/abs/1989ApJ...342..379W for more details
    about Hillas parameters.

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    namedtuple
        The score of the image cleaning algorithm for the given image.
    """

    # Copy and cast images to prevent tricky bugs
    # See https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html#numpy-ndarray-astype
    output_image = output_image.astype('float64', copy=True)
    reference_image = reference_image.astype('float64', copy=True)

    if params is not None and "kill" in params and params["kill"]:
        # Remove isolated pixels on the reference image before assessment.
        reference_image = kill_isolated_pixels(reference_image, threshold=params["kill_threshold"])

    if params is not None and "hillas_implementation" in params and params["hillas_implementation"] in (1, 2):
        # Remove isolated pixels on the reference image before assessment.
        hillas_implementation = params["hillas_implementation"]
    else:
        hillas_implementation = 2

    output_image_parameters = get_hillas_parameters(output_image, hillas_implementation, pixels_position)
    reference_image_parameters = get_hillas_parameters(reference_image, hillas_implementation, pixels_position)

    #print(reference_image_parameters)

    # Size
    output_image_parameter_size = float(output_image_parameters.size)
    reference_image_parameter_size = float(reference_image_parameters.size)
    delta_size = reference_image_parameter_size - output_image_parameter_size

    # Centroid x
    output_image_parameter_cen_x = output_image_parameters.cen_x.value
    reference_image_parameter_cen_x = reference_image_parameters.cen_x.value
    delta_cen_x = reference_image_parameter_cen_x - output_image_parameter_cen_x

    # Centroid y
    output_image_parameter_cen_y = output_image_parameters.cen_y.value
    reference_image_parameter_cen_y = reference_image_parameters.cen_y.value
    delta_cen_y = reference_image_parameter_cen_y - output_image_parameter_cen_y

    # Length
    output_image_parameter_length = output_image_parameters.length.value
    reference_image_parameter_length = reference_image_parameters.length.value
    delta_length = reference_image_parameter_length - output_image_parameter_length

    # Width
    output_image_parameter_width = output_image_parameters.width.value
    reference_image_parameter_width = reference_image_parameters.width.value
    delta_width = reference_image_parameter_width - output_image_parameter_width

    # R
    output_image_parameter_r = output_image_parameters.r.value
    reference_image_parameter_r = reference_image_parameters.r.value
    delta_r = reference_image_parameter_r - output_image_parameter_r

    # Phi
    output_image_parameter_phi = output_image_parameters.phi.to(u.rad).value
    reference_image_parameter_phi = reference_image_parameters.phi.to(u.rad).value
    delta_phi = reference_image_parameter_phi - output_image_parameter_phi

    # Psi (shower direction angle)
    output_image_parameter_psi_rad = output_image_parameters.psi.to(u.rad).value
    reference_image_parameter_psi_rad = reference_image_parameters.psi.to(u.rad).value
    delta_psi_rad = reference_image_parameter_psi_rad - output_image_parameter_psi_rad

    # Normalized psi
    normalized_delta_psi = norm_angle_diff(math.degrees(delta_psi_rad))

    ## Miss
    #output_image_parameter_miss = output_image_parameters.miss.value
    #reference_image_parameter_miss = reference_image_parameters.miss.value
    #delta_miss = reference_image_parameter_miss - output_image_parameter_miss

    if params is not None and "kill" in params and params["kill"]:
        suffix_str = '_kill'
    else:
        suffix_str = ''

    score_dict = collections.OrderedDict((
                    ('hillas' + str(hillas_implementation) + '_delta_size'     + suffix_str, delta_size),
                    ('hillas' + str(hillas_implementation) + '_delta_cen_x'    + suffix_str, delta_cen_x),
                    ('hillas' + str(hillas_implementation) + '_delta_cen_y'    + suffix_str, delta_cen_y),
                    ('hillas' + str(hillas_implementation) + '_delta_length'   + suffix_str, delta_length),
                    ('hillas' + str(hillas_implementation) + '_delta_width'    + suffix_str, delta_width),
                    ('hillas' + str(hillas_implementation) + '_delta_r'        + suffix_str, delta_r),
                    ('hillas' + str(hillas_implementation) + '_delta_phi'      + suffix_str, delta_phi),
                    ('hillas' + str(hillas_implementation) + '_delta_psi'      + suffix_str, delta_psi_rad),
                    ('hillas' + str(hillas_implementation) + '_delta_psi_norm' + suffix_str, normalized_delta_psi),
                    #('hillas' + str(hillas_implementation) + '_delta_miss'    + suffix_str, delta_miss)
                 ))

    Score = collections.namedtuple('Score', score_dict.keys())

    return Score(**score_dict)


# Hillas delta 2 ##############################################################

def metric_hillas_delta2(input_img, output_image, reference_image, pixels_position, params=None):
    r"""Compute the score of ``output_image`` regarding ``reference_image``
    with the *Hillas parameters*.

    It works exactly like :func:`metric_hillas_delta` except that isolated
    pixels are removed from the ``reference_image`` before the evaluation
    (using :func:`datapipe.image.kill_isolated_pixels`).

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_image: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_image: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    namedtuple
        The score of the image cleaning algorithm for the given image.
    """

    if params is None:
        params = {}

    params["kill"] = True
    params["kill_threshold"] = 0.2   # TODO: don't give an hardcoded value

    scores = metric_hillas_delta(input_img, output_image, reference_image, pixels_position, params)

    return scores


# Kill isolated pixels ########################################################

def metric_kill_isolated_pixels(input_img, output_image, reference_image, pixels_position=None, params=None):
    delta_pe, delta_abs_pe, delta_num_pixels = kill_isolated_pixels_stats(output_image)

    score_dict = collections.OrderedDict((
                    ('kill_isolated_pixels_delta_pe',         delta_pe),
                    ('kill_isolated_pixels_delta_abs_pe',     delta_abs_pe),
                    ('kill_isolated_pixels_delta_num_pixels', delta_num_pixels)
                 ))

    Score = collections.namedtuple('Score', score_dict.keys())

    return Score(**score_dict)

###############################################################################
# ASSESS FUNCTIONS DRIVER                                                     #
###############################################################################

BENCHMARK_DICT = {
    "mse":                  (metric_mse,),
    "nrmse":                (metric_nrmse,),
    "unrmse":               (metric1,),
    "e_shape":              (metric2,),
    "e_energy":             (metric3,),
    "mpdspd":               (metric2, metric3),
    "sspd":                 (metric4,),
    "ssim":                 (metric_ssim,),
    "psnr":                 (metric_psnr,),
    "delta_psi":            (metric_delta_psi,),
    "hillas_delta":         (metric_hillas_delta,),
    "hillas_delta2":        (metric_hillas_delta2,),
    "kill_isolated_pixels": (metric_kill_isolated_pixels,),
    "all":                  (metric_mse, metric_nrmse, metric2, metric3, metric4, metric_ssim, metric_psnr, metric_hillas_delta, metric_hillas_delta2, metric_kill_isolated_pixels)
}

METRIC_NAME_DICT = {
    metric_mse:                  "mse",
    metric_nrmse:                "nrmse",
    metric1:                     "unrmse",
    metric2:                     "e_shape",
    metric3:                     "e_energy",
    metric4:                     "sspd",
    metric_ssim:                 "ssim",
    metric_psnr:                 "psnr",
    metric_delta_psi:            "delta_psi",
    metric_hillas_delta:         "hillas_delta",
    metric_hillas_delta2:        "hillas_delta2",
    metric_kill_isolated_pixels: "kill_isolated_pixels"
}

def assess_image_cleaning(input_img, output_img, reference_img, pixels_position, benchmark_method, params=None):
    r"""Compute the score of `output_image` regarding `reference_image`
    with the `benchmark_method` metrics:

    - "mse":                  :func:`metric_mse`
    - "nrmse":                :func:`metric_nrmse`
    - "unrmse":               :func:`metric1`
    - "e_shape":              :func:`metric2`
    - "e_energy":             :func:`metric3`
    - "mpdspd":               :func:`metric2`, :func:`metric3`
    - "sspd":                 :func:`metric4`
    - "ssim":                 :func:`metric_ssim`
    - "psnr":                 :func:`metric_psnr`
    - "delta_psi":            :func:`metric_delta_psi`
    - "hillas_delta":         :func:`metric_hillas_delta`
    - "hillas_delta2":        :func:`metric_hillas_delta2`
    - "kill_isolated_pixels": :func:`metric_kill_isolated_pixels`
    - "all":                  :func:`metric_mse`, :func:`metric_nrmse`, :func:`metric2`, :func:`metric3`, :func:`metric4`, :func:`metric_ssim`, :func:`metric_psnr`, :func:`metric_hillas_delta`, :func:`metric_hillas_delta2`, :func:`metric_kill_isolated_pixels`

    Parameters
    ----------
    input_img: 2D ndarray
        The RAW original image.
    output_img: 2D ndarray
        The cleaned image returned by the image cleanning algorithm to assess.
    reference_img: 2D ndarray
        The actual clean image (the best result that can be expected for the
        image cleaning algorithm).
    params: dict
        Additional options.

    Returns
    -------
    tuple of float numbers
        The score(s) of the image cleaning algorithm for the given image.
    """

    try:
        score_list = []
        metric_name_list = []

        for metric_function in BENCHMARK_DICT[benchmark_method]:
            score = metric_function(input_img, output_img, reference_img, pixels_position, params) 

            if isinstance(score, collections.Sequence):
                score_list.extend(score)
                metric_name_list.extend(score._fields)
            else:
                score_list.append(score)
                metric_name_list.append(METRIC_NAME_DICT[metric_function])

        assert len(score_list) == len(metric_name_list)
    except KeyError as e:
        raise UnknownMethod()

    #for s, m in zip(score_list, metric_name_list):
    #    print(m, ":", s, type(s))

    return tuple(score_list), tuple(metric_name_list)

