#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

./datapipe/denoising/fft.py -b1 -s -t0.004 ~/data/astri_mini_array/fits/gamma/*.fits
./datapipe/denoising/tailcut.py -b1 -T0.75 -t0.5 ~/data/astri_mini_array/fits/gamma/*.fits
./datapipe/denoising/wavelets_mrtransform.py -b1 -n5 ~/data/astri_mini_array/fits/gamma/*.fits
