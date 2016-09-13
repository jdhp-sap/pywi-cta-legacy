#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

#./datapipe/denoising/fft.py -b1 -s -t0.004           $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/tailcut.py -b1 -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/wavelets_mrtransform.py -b1 -n5 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)

#./datapipe/denoising/fft.py -b2 -s -t0.004           $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/tailcut.py -b2 -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/wavelets_mrtransform.py -b2 -n5 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n 2203)

./datapipe/denoising/fft.py -b1 -s -t0.004           $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)
./datapipe/denoising/tailcut.py -b1 -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)
./datapipe/denoising/wavelets_mrtransform.py -b1 -n5 $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)

#./datapipe/denoising/fft.py -b2 -s -t0.004           $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/tailcut.py -b2 -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)
#./datapipe/denoising/wavelets_mrtransform.py -b2 -n5 $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n 2203)
