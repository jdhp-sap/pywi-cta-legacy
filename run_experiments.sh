#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

INFILE=$1
#INFILE=data/CT062.fits

./datapipe/denoising/tailcut.py -T 0.75 -t 0.5 "${INFILE}"
./datapipe/denoising/fft.py -s -t 0.02 "${INFILE}"
./datapipe/denoising/wavelets_mrtransform.py "${INFILE}"
