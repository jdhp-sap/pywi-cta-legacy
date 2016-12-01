#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

# PLOT SCORES #####

echo "" # & echo "* SCORE PROTON MPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   --title "Score MPD (protons)"        -o score_proton_mpd_boxplot.pdf                       score_proton_mpd_*.json
echo "" # & echo "* SCORE PROTON MPDSPD I0 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ (protons)"  -o score_proton_mpdspd_i0_boxplot.pdf                 score_proton_mpdspd_*.json
echo "" # & echo "* SCORE PROTON MPDSPD I1 BOXPLOT *****" & ./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ (protons)"  -o score_proton_mpdspd_i1_boxplot.pdf                 score_proton_mpdspd_*.json
echo "" # & echo "* SCORE PROTON SSPD BOXPLOT **********" & ./utils/plot_score_boxplot.py   -q                   --title "Score SSPD (protons)"       -o score_proton_sspd_boxplot.pdf                      score_proton_sspd_*.json

echo "" # & echo "* SCORE PROTON MPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q --logx --logy     --title "Score MPD (protons)"        -o score_proton_mpd_histogram.pdf                     score_proton_mpd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I0 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q        --logy -i0 --title "$\mathcal{E}_1$ (protons)"  -o score_proton_mpdspd_i0_histogram.pdf               score_proton_mpdspd_*.json
echo ""   & echo "* SCORE PROTON MPDSPD I1 HISTOGRAM ***" & ./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ (protons)"  -o score_proton_mpdspd_i1_histogram.pdf               score_proton_mpdspd_*.json
echo "" # & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "FFT"                        -o score_proton_sspd_histogram_fft.pdf                score_proton_sspd_fft.json
echo ""   & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "Tailcut (JD)"               -o score_proton_sspd_histogram_tailcut_jd.pdf         score_proton_sspd_tailcut_jd.json
echo ""   & echo "* SCORE PROTON SSPD HISTOGRAM ********" & ./utils/plot_score_histogram.py -q        --logy     --title "WT"                         -o score_proton_sspd_histogram_wavelets_mrfilter.pdf  score_proton_sspd_wavelets_mrfilter.json

echo "" # & echo "* SCORE GAMMA MPD BOXPLOT ************" & ./utils/plot_score_boxplot.py   -q                   --title "Score MPD ($\gamma$)"       -o score_gamma_mpd_boxplot.pdf                        score_gamma_mpd_*.json
echo "" # & echo "* SCORE GAMMA MPDSPD I0 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o score_gamma_mpdspd_i0_boxplot.pdf                  score_gamma_mpdspd_*.json
echo "" # & echo "* SCORE GAMMA MPDSPD I1 BOXPLOT ******" & ./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o score_gamma_mpdspd_i1_boxplot.pdf                  score_gamma_mpdspd_*.json
echo "" # & echo "* SCORE GAMMA SSPD BOXPLOT ***********" & ./utils/plot_score_boxplot.py   -q                   --title "Score SSPD ($\gamma$)"      -o score_gamma_sspd_boxplot.pdf                       score_gamma_sspd_*.json

echo "" # & echo "* SCORE GAMMA MPD HISTOGRAM **********" & ./utils/plot_score_histogram.py -q --logx --logy     --title "Score MPD ($\gamma$)"       -o score_gamma_mpd_histogram.pdf                      score_gamma_mpd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I0 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q        --logy -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o score_gamma_mpdspd_i0_histogram.pdf                score_gamma_mpdspd_*.json
echo ""   & echo "* SCORE GAMMA MPDSPD I1 HISTOGRAM ****" & ./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o score_gamma_mpdspd_i1_histogram.pdf                score_gamma_mpdspd_*.json
echo "" # & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "FFT"                        -o score_gamma_sspd_histogram_fft.pdf                 score_gamma_sspd_fft.json
echo ""   & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "Tailcut (JD)"               -o score_gamma_sspd_histogram_tailcut_jd.pdf          score_gamma_sspd_tailcut_jd.json
echo ""   & echo "* SCORE GAMMA SSPD HISTOGRAM *********" & ./utils/plot_score_histogram.py -q        --logy     --title "WT"                         -o score_gamma_sspd_histogram_wavelets_mrfilter.pdf   score_gamma_sspd_wavelets_mrfilter.json


./utils/plot_score_histogram2d.py --key "npe" --logx --logy -i0 --title "$\mathcal{E}_1$ ($\gamma$)"     -q -o score_gamma_mpdspd_i0_histogram2d.pdf   score_gamma_mpdspd_tailcut_jd.json   score_gamma_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy -i1 --title "$\mathcal{E}_2$ ($\gamma$)"     -q -o score_gamma_mpdspd_i1_histogram2d.pdf   score_gamma_mpdspd_tailcut_jd.json   score_gamma_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe"        --logy     --title "Energy conservation ($\gamma$)" -q -o score_gamma_sspd_histogram2d.pdf        score_gamma_sspd_tailcut_jd.json     score_gamma_sspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy -i0 --title "$\mathcal{E}_1$ (protons)"      -q -o score_proton_mpdspd_i0_histogram2d.pdf  score_proton_mpdspd_tailcut_jd.json  score_proton_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy -i1 --title "$\mathcal{E}_2$ (protons)"      -q -o score_proton_mpdspd_i1_histogram2d.pdf  score_proton_mpdspd_tailcut_jd.json  score_proton_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe"        --logy     --title "Energy conservation (protons)"  -q -o score_proton_sspd_histogram2d.pdf       score_proton_sspd_tailcut_jd.json    score_proton_sspd_wavelets_mrfilter.json

./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i0 --title "$\mathcal{E}_1$ ($\gamma$)"     -q -o score_gamma_mpdspd_i0_histogram2d_logz.pdf   score_gamma_mpdspd_tailcut_jd.json   score_gamma_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i1 --title "$\mathcal{E}_2$ ($\gamma$)"     -q -o score_gamma_mpdspd_i1_histogram2d_logz.pdf   score_gamma_mpdspd_tailcut_jd.json   score_gamma_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe"        --logy --logz     --title "Energy conservation ($\gamma$)" -q -o score_gamma_sspd_histogram2d_logz.pdf        score_gamma_sspd_tailcut_jd.json     score_gamma_sspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i0 --title "$\mathcal{E}_1$ (protons)"      -q -o score_proton_mpdspd_i0_histogram2d_logz.pdf  score_proton_mpdspd_tailcut_jd.json  score_proton_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i1 --title "$\mathcal{E}_2$ (protons)"      -q -o score_proton_mpdspd_i1_histogram2d_logz.pdf  score_proton_mpdspd_tailcut_jd.json  score_proton_mpdspd_wavelets_mrfilter.json
./utils/plot_score_histogram2d.py --key "npe"        --logy --logz     --title "Energy conservation (protons)"  -q -o score_proton_sspd_histogram2d_logz.pdf       score_proton_sspd_tailcut_jd.json    score_proton_sspd_wavelets_mrfilter.json


./utils/plot_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ ($\gamma$)" -q -o score_gamma_npe.pdf   score_gamma_mpdspd_tailcut_jd.json
./utils/plot_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ (protons)"  -q -o score_proton_npe.pdf  score_proton_mpdspd_tailcut_jd.json


#./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_gamma_mpdspd_correlation_fft.pdf        ./score_gamma_mpdspd_fft.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_gamma_mpdspd_correlation_null.pdf       ./score_gamma_mpdspd_null.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_gamma_mpdspd_correlation_tailcut_jd.pdf ./score_gamma_mpdspd_tailcut_jd.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_gamma_mpdspd_correlation_wt.pdf         ./score_gamma_mpdspd_wavelets_mrfilter.json

#./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_proton_mpdspd_correlation_fft.pdf        ./score_proton_mpdspd_fft.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_proton_mpdspd_correlation_null.pdf       ./score_proton_mpdspd_null.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_proton_mpdspd_correlation_tailcut_jd.pdf ./score_proton_mpdspd_tailcut_jd.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o score_proton_mpdspd_correlation_wt.pdf         ./score_proton_mpdspd_wavelets_mrfilter.json
