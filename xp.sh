#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NUM_IMG=100

TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#WT_MR_FILTER_PARAMS="-n4 -K -k -C2 -m3 --kill-isolated-pixels"
#WT_MR_FILTER_PARAMS="-n4 -K -k -C2 -m3 --kill-isolated-pixels --offset-after-calibration=10"
#WT_MR_FILTER_PARAMS="-n4 -K -k -C1 -s3 -m3 --kill-isolated-pixels --offset-after-calibration=10"

###################
# GAMMAS ##########
###################

echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_gamma_all_null_ref.json                 $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_null_ref.json.log
echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_gamma_all_null_input.json               $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_null_input.json.log

TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_gamma_all_tailcut_ref.json              $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_tailcut_ref.json.log

TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_gamma_all_tailcut_kill.json             $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_tailcut_kill.json.log

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_gamma_all_wavelets_mrfilter_ref.json    $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_wavelets_mrfilter_ref.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

###################
# PROTONS #########
###################

echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_proton_all_null_ref.json                 $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_null_ref.json.log
echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_proton_all_null_input.json               $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_null_input.json.log

TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_proton_all_tailcut_ref.json              $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_tailcut_ref.json.log

TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_proton_all_tailcut_kill.json             $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_tailcut_kill.json.log

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_proton_all_wavelets_mrfilter_ref.json    $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_wavelets_mrfilter_ref.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_kill.json   $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

####################
## ALL GAMMAS ######
####################
#
#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_gamma_all_null_ref.json                 ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_gamma_all_null_input.json               ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_input.json.log
#
#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_gamma_all_tailcut_ref.json              ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_tailcut_ref.json.log
#
#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_gamma_all_tailcut_kill.json             ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_tailcut_kill.json.log
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_gamma_all_wavelets_mrfilter_ref.json    ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#####################
## ALL PROTONS ######
#####################
#
#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py            -b all --label="Ref"                                -o score_proton_all_null_ref.json                 ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py                -b all --label="Input"                              -o score_proton_all_null_input.json               ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_input.json.log
#
#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}          -o score_proton_all_tailcut_ref.json              ~/astri_data/fits/proton 2>&1 | tee score_proton_all_tailcut_ref.json.log
#
#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}      -o score_proton_all_tailcut_kill.json             ~/astri_data/fits/proton 2>&1 | tee score_proton_all_tailcut_kill.json.log
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}     -o score_proton_all_wavelets_mrfilter_ref.json    ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS} -o score_proton_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
