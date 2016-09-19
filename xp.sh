#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=10

# PROTONS #########

echo "" # & echo "* MPD FFT"         & ./datapipe/denoising/fft.py                  -b mpd    -s -t0.004   -o score_proton_mpd_fft.json                      $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* MPD TAILCUT"     & ./datapipe/denoising/tailcut.py              -b mpd    -T0.75 -t0.5 -o score_proton_mpd_tailcut.json                  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrtransform.py -b mpd    -n5          -o score_proton_mpd_wavelets_mrtransform.json     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & rm *.fits

echo ""   & echo "* MPDSDP FFT"      & ./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_proton_mpdspd_fft.json                   $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_proton_mpdspd_tailcut.json               $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_proton_mpdspd_wavelets_mrtransform.json  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & rm *.fits

echo ""   & echo "* SSPD FFT"        & ./datapipe/denoising/fft.py                  -b sspd   -s -t0.004   -o score_proton_sspd_fft.json                     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* SSPD TAILCUT"    & ./datapipe/denoising/tailcut.py              -b sspd   -T0.75 -t0.5 -o score_proton_sspd_tailcut.json                 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrtransform.py -b sspd   -n5          -o score_proton_sspd_wavelets_mrtransform.json    $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & rm *.fits

# GAMMAS ##########

echo "" # & echo "* MPD FFT"         & ./datapipe/denoising/fft.py                  -b mpd    -s -t0.004   -o score_gamma_mpd_fft.json                       $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* MPD TAILCUT"     & ./datapipe/denoising/tailcut.py              -b mpd    -T0.75 -t0.5 -o score_gamma_mpd_tailcut.json                   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrtransform.py -b mpd    -n5          -o score_gamma_mpd_wavelets_mrtransform.json      $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & rm *.fits

echo ""   & echo "* MPDSDP FFT"      & ./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_gamma_mpdspd_fft.json                    $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_gamma_mpdspd_tailcut.json                $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_gamma_mpdspd_wavelets_mrtransform.json   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & rm *.fits

echo ""   & echo "* SSPD FFT"        & ./datapipe/denoising/fft.py                  -b sspd   -s -t0.004   -o score_gamma_sspd_fft.json                      $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* SSPD TAILCUT"    & ./datapipe/denoising/tailcut.py              -b sspd   -T0.75 -t0.5 -o score_gamma_sspd_tailcut.json                  $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrtransform.py -b sspd   -n5          -o score_gamma_sspd_wavelets_mrtransform.json     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & rm *.fits

# ALL GAMMAS ######

echo "" # & echo "* MPD FFT"         & ./datapipe/denoising/fft.py                  -b mpd -s -t0.004      -o score_gamma_mpd_fft.json                       ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* MPD TAILCUT"     & ./datapipe/denoising/tailcut.py              -b mpd -T0.75 -t0.5    -o score_gamma_mpd_tailcut.json                   ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrtransform.py -b mpd -n5             -o score_gamma_mpd_wavelets_mrtransform.json      ~/data/astri_mini_array/fits/gamma
echo "" # & rm *.fits

echo "" # & echo "* MPDSDP FFT"      & ./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_gamma_mpdspd_fft.json                    ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_gamma_mpdspd_tailcut.json                ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_gamma_mpdspd_wavelets_mrtransform.json   ~/data/astri_mini_array/fits/gamma
echo "" # & rm *.fits

echo "" # & echo "* SSPD FFT"        & ./datapipe/denoising/fft.py                  -b sspd -s -t0.004     -o score_gamma_sspd_fft.json                      ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* SSPD TAILCUT"    & ./datapipe/denoising/tailcut.py              -b sspd -T0.75 -t0.5   -o score_gamma_sspd_tailcut.json                  ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrtransform.py -b sspd -n5            -o score_gamma_sspd_wavelets_mrtransform.json     ~/data/astri_mini_array/fits/gamma
echo "" # & rm *.fits

