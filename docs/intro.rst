.. currentmodule:: datapipe

============
Introduction
============

Signal processing for gamma-ray science.

Note:

    This project is in beta stage.


* Online documentation: http://datapipe.readthedocs.org
* Source code: https://github.com/jdhp-sap/sap-cta-data-pipeline
* Issue tracker: https://github.com/jdhp-sap/sap-cta-data-pipeline/issues
* datapipe on PyPI: https://pypi.python.org/pypi/datapipe


Dependencies
============

*  Python >= 3.0

.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall SAp CTA data pipeline with these commands (in a
terminal)::

    pip install --pre datapipe
    pip install --upgrade datapipe
    pip uninstall datapipe

Or, if you have downloaded the SAp CTA data pipeline source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install datapipe

Windows
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.4 under Windows 7.
..     It should also work with recent Windows systems.

You can install, upgrade, uninstall SAp CTA data pipeline with these commands (in a
`command prompt`_)::

    py -m pip install --pre datapipe
    py -m pip install --upgrade datapipe
    py -m pip uninstall datapipe

Or, if you have downloaded the SAp CTA data pipeline source code::

    py setup.py install

MacOSX
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.5 under MacOSX 10.9 (*Mavericks*).
..     It should also work with recent MacOSX systems.

You can install, upgrade, uninstall SAp CTA data pipeline with these commands (in a
terminal)::

    pip install --pre datapipe
    pip install --upgrade datapipe
    pip uninstall datapipe

Or, if you have downloaded the SAp CTA data pipeline source code::

    python3 setup.py install

Image cleaning guidelines
=========================

Here is the basic guidelines to clean images (and assess cleaning algorithms).

Step 1
------

Extract images from Simtel files, crop them, convert them to "regular" 2D
images and write them into fits files (one fits file per image with the ADC
signal in HDU0 and the photoelectron signal in HDU1):

1. clone http://github.com/jdhp-sap/snippets
2. check snippets/ctapipe/extract_and_crop_simtel_images.py on lines 64 and 66,
   these lines may need to be fixed
3. in snippets/ctapipe run ``./extract_crop_and_plot_all_astri_images.sh ASTRI_SIMTEL_FILE``

Step 1.4 generate a lot of fits files in your current directory ;
its execution may be long (up to several hours) as the script is not optimized
at all and many instructions are redundant (but this is not a big deal because
you only need to run it once to generate your input files).

Step 2
------

Install mr_transform (the cosmostat wavelet transform tool):

1. download http://www.cosmostat.org/wp-content/uploads/2014/12/ISAP_V3.1.tgz (see http://www.cosmostat.org/software/isap/)
2. unzip this archive, go to the "sparse2d" directory and compile the sparse2d
   library. It should generate an executable named "mr_transform"::

    tar -xzvf ISAP_V3.1.tgz
    cd ISAP_V3.1/cxx
    tar -xzvf sparse2d_V1.1.tgz
    cd sparse2d
    compile the content of this directory

Step 3
------

Clean images generated in step 1:

1. clone and install
   http://github.com/jdhp-sap/data-pipeline-standalone-scripts (see
   https://github.com/jdhp-sap/data-pipeline-standalone-scripts#installation)
2. to clean one fits file (see for instance run_experiments.sh):

   - with Tailcut : in data-pipeline-standalone-scripts, run ``./datapipe/denoising/tailcut.py -T 0.75 -t 0.5 FITS_FILE`` (-T = max threshold, -t = min threshold, use the -h option to see command usage)
   - with FFT : in data-pipeline-standalone-scripts, run ``./datapipe/denoising/fft.py -s -t 0.02 FITS_FILE`` (-t = threshold in the Fourier space, use the -h option to see command usage)
   - with Wavelets : in data-pipeline-standalone-scripts, run ``./datapipe/denoising/wavelets_mrtrransform.py FITS_FILE`` (use the -h option to see command usage)

3. instead of the step 3.2, the "benchmark mode" can be set to clean
   images and assess cleaning algorithms (it's still a bit experimental) : use
   the same instructions than for step 3.2 with the additional option "-b 1" in
   each command (and put several fits files in input e.g. "*.fits")

Step 4
------

Optionally, plot some stats about scores:
in data-pipeline-standalone-scripts/utils, use the plot_score_*.py scripts on
the JSON files generated in step 3.3 (use the -h option to see command usage)


Bug reports
===========

To search for bugs or report them, please use the SAp Data Pipeline Standalone
Scripts Bug Tracker at:

    https://github.com/jdhp-sap/sap-cta-data-pipeline/issues


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Credits
=======

Created by `Jérémie Decock`_ and Tino Michael.


.. _Jérémie Decock: http://www.jdhp.org
.. _SAp CTA data pipeline: http://www.jdhp.org/software_en.html#datapipe
