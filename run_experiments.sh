#!/bin/sh

INFILE=data/CT062.fits

./datapipe/denoising/tailcut -T 0.75 -t 0.5 "${INFILE}"
./datapipe/denoising/fft.py -s -t 0.02 "${INFILE}"
./datapipe/denoising/wavelets_mrtransform.py "${INFILE}"
