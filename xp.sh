#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=100

# PROTONS

./datapipe/denoising/fft.py                  -b mpd    -s -t0.004   -o score_proton_mpd_fft.json                      $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b mpd    -T0.75 -t0.5 -o score_proton_mpd_tailcut.json                  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b mpd    -n5          -o score_proton_mpd_wavelets_mrtransform.json     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_proton_mpdspd_fft.json                   $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_proton_mpdspd_tailcut.json               $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_proton_mpdspd_wavelets_mrtransform.json  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

./datapipe/denoising/fft.py                  -b sspd   -s -t0.004   -o score_proton_sspd_fft.json                     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b sspd   -T0.75 -t0.5 -o score_proton_sspd_tailcut.json                 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b sspd   -n5          -o score_proton_sspd_wavelets_mrtransform.json    $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

# GAMMAS

./datapipe/denoising/fft.py                  -b mpd    -s -t0.004   -o score_gamma_mpd_fft.json                       $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b mpd    -T0.75 -t0.5 -o score_gamma_mpd_tailcut.json                   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b mpd    -n5          -o score_gamma_mpd_wavelets_mrtransform.json      $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_gamma_mpdspd_fft.json                    $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_gamma_mpdspd_tailcut.json                $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_gamma_mpdspd_wavelets_mrtransform.json   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

./datapipe/denoising/fft.py                  -b sspd   -s -t0.004   -o score_gamma_sspd_fft.json                      $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/tailcut.py              -b sspd   -T0.75 -t0.5 -o score_gamma_sspd_tailcut.json                  $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
./datapipe/denoising/wavelets_mrtransform.py -b sspd   -n5          -o score_gamma_sspd_wavelets_mrtransform.json     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
rm *.fits

# ALL GAMMAS

#./datapipe/denoising/fft.py                  -b mpd -s -t0.004      -o score_gamma_mpd_fft.json                       ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py              -b mpd -T0.75 -t0.5    -o score_gamma_mpd_tailcut.json                   ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b mpd -n5             -o score_gamma_mpd_wavelets_mrtransform.json      ~/data/astri_mini_array/fits/gamma
#rm *.fits

#./datapipe/denoising/fft.py                  -b mpdspd -s -t0.004   -o score_gamma_mpdspd_fft.json                    ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py              -b mpdspd -T0.75 -t0.5 -o score_gamma_mpdspd_tailcut.json                ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b mpdspd -n5          -o score_gamma_mpdspd_wavelets_mrtransform.json   ~/data/astri_mini_array/fits/gamma
#rm *.fits

#./datapipe/denoising/fft.py                  -b sspd -s -t0.004     -o score_gamma_sspd_fft.json                      ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/tailcut.py              -b sspd -T0.75 -t0.5   -o score_gamma_sspd_tailcut.json                  ~/data/astri_mini_array/fits/gamma
#./datapipe/denoising/wavelets_mrtransform.py -b sspd -n5            -o score_gamma_sspd_wavelets_mrtransform.json     ~/data/astri_mini_array/fits/gamma
#rm *.fits

# PLOT SCORES

echo "" & echo "* SCORE PROTON MPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   -o score_proton_mpd_boxplot.pdf         score_proton_mpd_*.json
echo "" & echo "* SCORE PROTON MPDSDP I0 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i0 -o score_proton_mpdspd_i0_boxplot.pdf   score_proton_mpdspd_*.json
echo "" & echo "* SCORE PROTON MPDSDP I1 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i1 -o score_proton_mpdspd_i1_boxplot.pdf   score_proton_mpdspd_*.json
echo "" & echo "* SCORE PROTON SSPD BOXPLOT **********" & ./utils/plot_score_boxplot.py   -q                   -o score_proton_sspd_boxplot.pdf        score_proton_sspd_*.json

echo "" & echo "* SCORE PROTON MPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q --logx --logy     -o score_proton_mpd_histogram.pdf       score_proton_mpd_*.json
echo "" & echo "* SCORE PROTON MPDSDP I0 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q --logx --logy -i0 -o score_proton_mpdspd_i0_histogram.pdf score_proton_mpdspd_*.json
echo "" & echo "* SCORE PROTON MPDSDP I1 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q --logx --logy -i1 -o score_proton_mpdspd_i1_histogram.pdf score_proton_mpdspd_*.json
echo "" & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     -o score_proton_sspd_histogram.pdf      score_proton_sspd_*.json

echo "" & echo "* SCORE GAMMA MPD BOXPLOT ************" & ./utils/plot_score_boxplot.py   -q                   -o score_gamma_mpd_boxplot.pdf          score_gamma_mpd_*.json
echo "" & echo "* SCORE GAMMA MPDSDP I0 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i0 -o score_gamma_mpdspd_i0_boxplot.pdf    score_gamma_mpdspd_*.json
echo "" & echo "* SCORE GAMMA MPDSDP I1 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i1 -o score_gamma_mpdspd_i1_boxplot.pdf    score_gamma_mpdspd_*.json
echo "" & echo "* SCORE GAMMA SSPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   -o score_gamma_sspd_boxplot.pdf         score_gamma_sspd_*.json

echo "" & echo "* SCORE GAMMA MPD HISTOGRAM **********" & ./utils/plot_score_histogram.py -q --logx --logy     -o score_gamma_mpd_histogram.pdf        score_gamma_mpd_*.json
echo "" & echo "* SCORE GAMMA MPDSDP I0 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q --logx --logy -i0 -o score_gamma_mpdspd_i0_histogram.pdf  score_gamma_mpdspd_*.json
echo "" & echo "* SCORE GAMMA MPDSDP I1 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q --logx --logy -i1 -o score_gamma_mpdspd_i1_histogram.pdf  score_gamma_mpdspd_*.json
echo "" & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     -o score_gamma_sspd_histogram.pdf       score_gamma_sspd_*.json

