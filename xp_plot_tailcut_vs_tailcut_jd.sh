#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

# PLOT SCORES #####

./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ (protons)"  -o 2016_10_18_tailcut_long/score_proton_mpdspd_i0_boxplot.pdf          2016_10_18_tailcut_long/score_proton_mpdspd_*.json
./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ (protons)"  -o 2016_10_18_tailcut_long/score_proton_mpdspd_i1_boxplot.pdf          2016_10_18_tailcut_long/score_proton_mpdspd_*.json
./utils/plot_score_boxplot.py   -q                   --title "Score SSPD (protons)"       -o 2016_10_18_tailcut_long/score_proton_sspd_boxplot.pdf               2016_10_18_tailcut_long/score_proton_sspd_*.json
                                                                                                                     
./utils/plot_score_histogram.py -q        --logy -i0 --title "$\mathcal{E}_1$ (protons)"  -o 2016_10_18_tailcut_long/score_proton_mpdspd_i0_histogram.pdf        2016_10_18_tailcut_long/score_proton_mpdspd_*.json
./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ (protons)"  -o 2016_10_18_tailcut_long/score_proton_mpdspd_i1_histogram.pdf        2016_10_18_tailcut_long/score_proton_mpdspd_*.json
./utils/plot_score_histogram.py -q        --logy     --title "Tailcut"                    -o 2016_10_18_tailcut_long/score_proton_sspd_histogram_tailcut.pdf     2016_10_18_tailcut_long/score_proton_sspd_tailcut.json
./utils/plot_score_histogram.py -q        --logy     --title "Tailcut (JD)"               -o 2018_10_18_tailcut_long/score_proton_sspd_histogram_tailcut_jd.pdf  2018_10_18_tailcut_long/score_proton_sspd_tailcut_jd.json
                                                                                                                     
./utils/plot_score_boxplot.py   -q               -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i0_boxplot.pdf           2016_10_18_tailcut_long/score_gamma_mpdspd_*.json
./utils/plot_score_boxplot.py   -q               -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i1_boxplot.pdf           2016_10_18_tailcut_long/score_gamma_mpdspd_*.json
./utils/plot_score_boxplot.py   -q                   --title "Score SSPD ($\gamma$)"      -o 2016_10_18_tailcut_long/score_gamma_sspd_boxplot.pdf                2016_10_18_tailcut_long/score_gamma_sspd_*.json
                                                                                                                     
./utils/plot_score_histogram.py -q        --logy -i0 --title "$\mathcal{E}_1$ ($\gamma$)" -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i0_histogram.pdf         2016_10_18_tailcut_long/score_gamma_mpdspd_*.json
./utils/plot_score_histogram.py -q --logx --logy -i1 --title "$\mathcal{E}_2$ ($\gamma$)" -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i1_histogram.pdf         2016_10_18_tailcut_long/score_gamma_mpdspd_*.json
./utils/plot_score_histogram.py -q        --logy     --title "Tailcut"                    -o 2016_10_18_tailcut_long/score_gamma_sspd_histogram_tailcut.pdf      2016_10_18_tailcut_long/score_gamma_sspd_tailcut.json
./utils/plot_score_histogram.py -q        --logy     --title "Tailcut (JD)"               -o 2016_10_18_tailcut_long/score_gamma_sspd_histogram_tailcut_jd.pdf   2016_10_18_tailcut_long/score_gamma_sspd_tailcut_jd.json


./utils/plot_score_histogram2d.py --key "npe" --logx --logy        -i0 --title "$\mathcal{E}_1$ ($\gamma$)"     -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i0_histogram2d.pdf        2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy        -i1 --title "$\mathcal{E}_2$ ($\gamma$)"     -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i1_histogram2d.pdf        2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe"        --logy            --title "Energy conservation ($\gamma$)" -q -o 2016_10_18_tailcut_long/score_gamma_sspd_histogram2d.pdf             2016_10_18_tailcut_long/score_gamma_sspd_tailcut_jd.json     2016_10_18_tailcut_long/score_gamma_sspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy        -i0 --title "$\mathcal{E}_1$ (protons)"      -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_i0_histogram2d.pdf       2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy        -i1 --title "$\mathcal{E}_2$ (protons)"      -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_i1_histogram2d.pdf       2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe"        --logy            --title "Energy conservation (protons)"  -q -o 2016_10_18_tailcut_long/score_proton_sspd_histogram2d.pdf            2016_10_18_tailcut_long/score_proton_sspd_tailcut_jd.json    2016_10_18_tailcut_long/score_proton_sspd_tailcut.json

./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i0 --title "$\mathcal{E}_1$ ($\gamma$)"     -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i0_histogram2d_logz.pdf   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i1 --title "$\mathcal{E}_2$ ($\gamma$)"     -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_i1_histogram2d_logz.pdf   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe"        --logy --logz     --title "Energy conservation ($\gamma$)" -q -o 2016_10_18_tailcut_long/score_gamma_sspd_histogram2d_logz.pdf        2016_10_18_tailcut_long/score_gamma_sspd_tailcut_jd.json     2016_10_18_tailcut_long/score_gamma_sspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i0 --title "$\mathcal{E}_1$ (protons)"      -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_i0_histogram2d_logz.pdf  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe" --logx --logy --logz -i1 --title "$\mathcal{E}_2$ (protons)"      -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_i1_histogram2d_logz.pdf  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_score_histogram2d.py --key "npe"        --logy --logz     --title "Energy conservation (protons)"  -q -o 2016_10_18_tailcut_long/score_proton_sspd_histogram2d_logz.pdf       2016_10_18_tailcut_long/score_proton_sspd_tailcut_jd.json    2016_10_18_tailcut_long/score_proton_sspd_tailcut.json


./utils/plot_image_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ ($\gamma$)" -q -o 2016_10_18_tailcut_long/score_gamma_npe_tc.pdf      2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_image_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ ($\gamma$)" -q -o 2016_10_18_tailcut_long/score_gamma_npe_tc_jd.pdf   2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json

./utils/plot_image_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ (protons)"  -q -o 2016_10_18_tailcut_long/score_proton_npe_tc.pdf     2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_image_metadata_histogram.py --key "npe" --logx --logy --exclude-aborted --title "$\sum_i s^*_i$ (protons)"  -q -o 2016_10_18_tailcut_long/score_proton_npe_tc_jd.pdf  2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json


./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_correlation_tailcut.pdf     2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o 2016_10_18_tailcut_long/score_gamma_mpdspd_correlation_tailcut_jd.pdf  2016_10_18_tailcut_long/score_gamma_mpdspd_tailcut_jd.json

./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_correlation_tailcut.pdf    2016_10_18_tailcut_long/score_proton_mpdspd_tailcut.json
./utils/plot_score_correlation.py --index1 0 --index2 1 --logx --logy -q -o 2016_10_18_tailcut_long/score_proton_mpdspd_correlation_tailcut_jd.pdf 2016_10_18_tailcut_long/score_proton_mpdspd_tailcut_jd.json
