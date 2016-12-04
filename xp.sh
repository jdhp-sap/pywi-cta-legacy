#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NUM_IMG=1000

TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
WT_MR_FILTER_PARAMS="-n4 -K -k -C1 -s3 -m3"  # 2016-10-19 REFERENCE
#WT_MR_FILTER_PARAMS="-n4 -K -k -C2 -m3 --kill-isolated-pixels --offset-after-calibration=10"
#WT_MR_FILTER_PARAMS="-n4 -K -k -C1 -s3 -m3 --kill-isolated-pixels --offset-after-calibration=10"

# PROTONS #########

#echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b all ${TAILCUT_PARAMS}       -o score_proton_mpdspd_tailcut_jd.json         $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all ${TAILCUT_PARAMS}       -o score_proton_mpdspd_tailcut.json            $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all ${WT_MR_FILTER_PARAMS}  -o score_proton_mpdspd_wavelets_mrfilter.json  $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
for FILE in .tmp*.fits ; do rm $FILE ; done

# GAMMAS ##########

#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b all ${TAILCUT_PARAMS}       -o score_gamma_mpdspd_tailcut_jd.json          $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all ${TAILCUT_PARAMS}       -o score_gamma_mpdspd_tailcut.json             $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all ${WT_MR_FILTER_PARAMS}  -o score_gamma_mpdspd_wavelets_mrfilter.json   $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
for FILE in .tmp*.fits ; do rm $FILE ; done

# ALL GAMMAS ######

#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b all ${TAILCUT_PARAMS}       -o score_gamma_mpdspd_tailcut_jd.json          ~/astri_data/fits/gamma
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all ${TAILCUT_PARAMS}       -o score_gamma_mpdspd_tailcut.json             ~/astri_data/fits/gamma
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all ${WT_MR_FILTER_PARAMS}  -o score_gamma_mpdspd_wavelets_mrfilter.json   ~/astri_data/fits/gamma
#for FILE in .tmp*.fits ; do rm $FILE ; done
