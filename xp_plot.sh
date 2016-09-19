#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

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

