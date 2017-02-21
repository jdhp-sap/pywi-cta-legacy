#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NUM_IMG=1000

TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#WT_MR_FILTER_PARAMS="-n4 -K -k -C2 -m3 --kill-isolated-pixels"
#WT_MR_FILTER_PARAMS="-n4 -K -k -C2 -m3 --kill-isolated-pixels --offset-after-calibration=10"
#WT_MR_FILTER_PARAMS="-n4 -K -k -C1 -s3 -m3 --kill-isolated-pixels --offset-after-calibration=10"

####################
## GAMMAS ##########
####################
#
#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_gamma_all_null_ref.json                 $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_gamma_all_null_input.json               $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_null_input.json.log
#
#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_gamma_all_tailcut_ref.json              $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_tailcut_ref.json.log
#
#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_gamma_all_tailcut_kill.json             $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_tailcut_kill.json.log
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_gamma_all_wavelets_mrfilter_ref.json    $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_gamma_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
####################
## PROTONS #########
####################
#
#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_proton_all_null_ref.json                 $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_proton_all_null_input.json               $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_null_input.json.log
#
#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_proton_all_tailcut_ref.json              $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_tailcut_ref.json.log
#
#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_proton_all_tailcut_kill.json             $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_tailcut_kill.json.log
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_proton_all_wavelets_mrfilter_ref.json    $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_kill.json   $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG}) | tee score_proton_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

###################
# ALL GAMMAS ######
###################

#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py           -b all --label="Ref"                                 -o score_gamma_all_null_ref.json                 ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py               -b all --label="Input"                               -o score_gamma_all_null_input.json               ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_input.json.log

#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}           -o score_gamma_all_tailcut_ref.json              ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_tailcut_ref.json.log

#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* GAMMA TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}       -o score_gamma_all_tailcut_kill.json             ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_tailcut_kill.json.log

#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}      -o score_gamma_all_wavelets_mrfilter_ref.json    ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

#WT_MR_FILTER_PARAMS="-K -f6 -m1 -n4 --kill-isolated-pixels"
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet_kill_f6_m1" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

#WT_MR_FILTER_PARAMS="-K -m1 -f2 -s2 -n4 -C2 --kill-isolated-pixels"
#echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet_fabio" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_fabio.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_fabio.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-ref-s3" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3 -s3 -n4 -f3 --kill-isolated-pixels"
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-ref-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s3 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl13.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl13.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s4 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s4" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl14.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl14.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s5 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s5" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl15.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl15.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s3 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl23.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl23.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s4 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s4" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl24.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl24.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s5 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* GAMMA WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s5" ${WT_MR_FILTER_PARAMS}  -o score_gamma_all_wavelets_mrfilter_jl25.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_wavelets_mrfilter_jl25.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

#####################
## ALL PROTONS ######
#####################
#
#echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py            -b all --label="Ref"                                -o score_proton_all_null_ref.json                 ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_ref.json.log
#echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py                -b all --label="Input"                              -o score_proton_all_null_input.json               ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_input.json.log

#TAILCUT_PARAMS="-T10 -t5"                    # REFERENCE
#echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut" ${TAILCUT_PARAMS}          -o score_proton_all_tailcut_ref.json              ~/astri_data/fits/proton 2>&1 | tee score_proton_all_tailcut_ref.json.log

#TAILCUT_PARAMS="-T10 -t5 --kill-isolated-pixels"
#echo "* PROTON TAILCUT"  & ./datapipe/denoising/tailcut.py           -b all --label="TailcutKill" ${TAILCUT_PARAMS}      -o score_proton_all_tailcut_kill.json             ~/astri_data/fits/proton 2>&1 | tee score_proton_all_tailcut_kill.json.log

#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4"  # 2016-10-19 REFERENCE
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet" ${WT_MR_FILTER_PARAMS}     -o score_proton_all_wavelets_mrfilter_ref.json    ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_ref.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

#WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WaveletKill" ${WT_MR_FILTER_PARAMS} -o score_proton_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

#WT_MR_FILTER_PARAMS="-K -f6 -m1 -n4 --kill-isolated-pixels"
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet_kill_f6_m1" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_kill.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#
#WT_MR_FILTER_PARAMS="-K -m1 -f2 -s2 -n4 -C2 --kill-isolated-pixels"
#echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="Wavelet_fabio" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_fabio.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_fabio.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -k -C1 -m3 -s3 -n4 --kill-isolated-pixels"
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-ref-s3" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3 -s3 -n4 -f3 --kill-isolated-pixels"
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-ref-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_kill.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_kill.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s3 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl13.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl13.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s4 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s4" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl14.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl14.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s5 -n4 -t24 -f3 --kill-isolated-pixels"             # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t24-f3-s5" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl15.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl15.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s3 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s3" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl23.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl23.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s4 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s4" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl24.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl24.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done

WT_MR_FILTER_PARAMS="-K -C1 -m3  -s5 -n4 -t28 -f3 -i10 -e0 --kill-isolated-pixels"    # Suggested by Jean-Luc (TODO: try to adapt -s)
echo "* PROTON WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="WT-t28-f3-s5" ${WT_MR_FILTER_PARAMS}  -o score_proton_all_wavelets_mrfilter_jl25.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_wavelets_mrfilter_jl25.json.log
for FILE in .tmp*.fits ; do rm $FILE ; done
