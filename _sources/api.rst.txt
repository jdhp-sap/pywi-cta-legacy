=========================
SAp CTA data pipeline API
=========================

.. module:: datapipe

The library provides classes which are usable by third party tools.

.. note::

    This project is still in *beta* stage, so the API is not finalized yet.

Benchmark package:

.. toctree::
   :maxdepth: 1

   datapipe.benchmark.assess <api_benchmark_assess>

Denoising package:

.. toctree::
   :maxdepth: 1

   datapipe.denoising.wavelets_mrfilter <api_filter_wavelet_mrfilter>
   datapipe.denoising.wavelets_mrtransform <api_filter_wavelet_mrtransform>
   datapipe.denoising.tailcut <api_filter_tailcut>
   datapipe.denoising.abstract_cleaning_algorithm <api_filter_abstract_cleaning_algorithm>
   datapipe.denoising.inverse_transform_sampling <api_filter_inverse_transform_sampling>

Image package:

.. toctree::
   :maxdepth: 1

   datapipe.image.hillas_parameters <api_image_hillas_parameters>
   datapipe.image.pixel_clusters <api_image_pixel_clusters>
   datapipe.image.signal_to_border_distance <api_image_signal_to_border_distance>

I/O package:

.. toctree::
   :maxdepth: 1

   datapipe.io.geometry_converter <api_io_geometry_converter>
   datapipe.io.images <api_io_images>

Optimization package:

.. toctree::
   :maxdepth: 1

   datapipe.optimization.bruteforce <api_optimization_bruteforce>
   datapipe.optimization.differential_evolution <api_optimization_differential_evolution>
   datapipe.optimization.saes <api_optimization_saes>
   datapipe.optimization.objectivefunc.tailcut_delta_psi <api_optimization_objectivefunc_tailcut_delta_psi>
   datapipe.optimization.objectivefunc.wavelets_mrfilter_delta_psi <api_optimization_objectivefunc_wavelets_mrfilter_delta_psi>

