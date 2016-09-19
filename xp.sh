#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=100

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

# PLOT SCORES #####

echo "" # & echo "* SCORE PROTON MPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   --title "Score MPD (protons)"        -o score_proton_mpd_boxplot.pdf                          score_proton_mpd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I0 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ (protons)"  -o score_proton_mpdspd_i0_boxplot.pdf                    score_proton_mpdspd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I1 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ (protons)"  -o score_proton_mpdspd_i1_boxplot.pdf                    score_proton_mpdspd_*.json
echo "" # & echo "* SCORE PROTON SSPD BOXPLOT **********" & ./utils/plot_score_boxplot.py   -q                   --title "Score SSPD (protons)"       -o score_proton_sspd_boxplot.pdf                         score_proton_sspd_*.json

echo "" # & echo "* SCORE PROTON MPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q --logx --logy     --title "Score MPD (protons)"        -o score_proton_mpd_histogram.pdf                        score_proton_mpd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I0 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q --logx --logy -i0 --title "$\mathcal{E}_1$ (protons)"  -o score_proton_mpdspd_i0_histogram.pdf                  score_proton_mpdspd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I1 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ (protons)"  -o score_proton_mpdspd_i1_histogram.pdf                  score_proton_mpdspd_*.json
echo ""   & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "FFT"                        -o score_proton_sspd_histogram_fft.pdf                   score_proton_sspd_fft.json
echo ""   & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "Tailcut"                    -o score_proton_sspd_histogram_tailcut.pdf               score_proton_sspd_tailcut.json
echo ""   & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "WT"                         -o score_proton_sspd_histogram_wavelets_mrtransform.pdf  score_proton_sspd_wavelets_mrtransform.json

echo "" # & echo "* SCORE GAMMA MPD BOXPLOT ************" & ./utils/plot_score_boxplot.py   -q                   --title "Score MPD ($\gamma$)"       -o score_gamma_mpd_boxplot.pdf                           score_gamma_mpd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I0 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o score_gamma_mpdspd_i0_boxplot.pdf                     score_gamma_mpdspd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I1 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o score_gamma_mpdspd_i1_boxplot.pdf                     score_gamma_mpdspd_*.json
echo "" # & echo "* SCORE GAMMA SSPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   --title "Score SSPD ($\gamma$)"      -o score_gamma_sspd_boxplot.pdf                          score_gamma_sspd_*.json

echo "" # & echo "* SCORE GAMMA MPD HISTOGRAM **********" & ./utils/plot_score_histogram.py -q --logx --logy     --title "Score MPD ($\gamma$)"       -o score_gamma_mpd_histogram.pdf                         score_gamma_mpd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I0 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q --logx --logy -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o score_gamma_mpdspd_i0_histogram.pdf                   score_gamma_mpdspd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I1 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o score_gamma_mpdspd_i1_histogram.pdf                   score_gamma_mpdspd_*.json
echo ""   & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "FFT"                        -o score_gamma_sspd_histogram_fft.pdf                    score_gamma_sspd_fft.json
echo ""   & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "Tailcut"                    -o score_gamma_sspd_histogram_tailcut.pdf                score_gamma_sspd_tailcut.json
echo ""   & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "WT"                         -o score_gamma_sspd_histogram_wavelets_mrtransform.pdf   score_gamma_sspd_wavelets_mrtransform.json

