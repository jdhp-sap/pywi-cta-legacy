#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=100

# PROTONS

#./datapipe/denoising/fft.py -b mpd -s -t0.004              $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/tailcut.py -b mpd -T0.75 -t0.5        $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/wavelets_mrtransform.py -b mpd -n5    $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#rm *.fits

#./datapipe/denoising/fft.py -b mpdspd -s -t0.004           $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/tailcut.py -b mpdspd -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
#rm *.fits

./datapipe/denoising/fft.py -b sspd -s -t0.004             $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py -b sspd -T0.75 -t0.5       $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b sspd -n5   $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

# GAMMAS

#./datapipe/denoising/fft.py -b mpd -s -t0.004              $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/tailcut.py -b mpd -T0.75 -t0.5        $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/wavelets_mrtransform.py -b mpd -n5    $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#rm *.fits

#./datapipe/denoising/fft.py -b mpdspd -s -t0.004           $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/tailcut.py -b mpdspd -T0.75 -t0.5     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5 $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
#rm *.fits

./datapipe/denoising/fft.py -b sspd -s -t0.004             $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py -b sspd -T0.75 -t0.5       $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b sspd -n5   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

# ALL GAMMAS

#./datapipe/denoising/fft.py -b mpd -s -t0.004              ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py -b mpd -T0.75 -t0.5        ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b mpd -n5    ~/data/astri_mini_array/fits/gamma
#rm *.fits

#./datapipe/denoising/fft.py -b mpdspd -s -t0.004           ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py -b mpdspd -T0.75 -t0.5     ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5 ~/data/astri_mini_array/fits/gamma
#rm *.fits

#./datapipe/denoising/fft.py -b sspd -s -t0.004             ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py -b sspd -T0.75 -t0.5       ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b sspd -n5   ~/data/astri_mini_array/fits/gamma
#rm *.fits
