#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NUM_IMG=500

TC_PARAMS="-T10 -t5 --kill-isolated-pixels"

WT_PARAMS_1="-K -k -C1 -m3 -n4 -s3       --kill-isolated-pixels"
WT_PARAMS_2="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels"

WT_LABEL_1="WT-K-k-C1-m3-n4-s3"
WT_LABEL_2="WT-K-k-C1-m3-n4-s2-2-3-3"

###################
# GAMMAS ##########
###################

echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_gamma_all_null_ref.json   $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_gamma_all_null_input.json $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* GAMMA TC"     & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_gamma_tc.json             $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_gamma_${WT_LABEL_2}.json  $(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
for FILE in .tmp*.fits ; do rm $FILE ; done

###################
# PROTONS #########
###################

echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_proton_all_null_ref.json   $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_proton_all_null_input.json $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* PROTON TC"    & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_proton_tc.json             $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_proton_${WT_LABEL_2}.json  $(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
for FILE in .tmp*.fits ; do rm $FILE ; done

####################
## ALL GAMMAS ######
####################
#
#echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_gamma_all_null_ref.json   ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_ref.jso.logn
#echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_gamma_all_null_input.json ~/astri_data/fits/gamma 2>&1 | tee score_gamma_all_null_input.json.log
#echo "* GAMMA TC"     & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_gamma_tc.json             ~/astri_data/fits/gamma 2>&1 | tee score_gamma_tc.json.log
#echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_gamma_${WT_LABEL_1}.json  ~/astri_data/fits/gamma 2>&1 | tee score_gamma_${WT_LABEL_1}.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_gamma_${WT_LABEL_2}.json  ~/astri_data/fits/gamma 2>&1 | tee score_gamma_${WT_LABEL_2}.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

######################
### ALL PROTONS ######
######################
#
#echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_proton_all_null_ref.json   ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_ref.jso.logn
#echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_proton_all_null_input.json ~/astri_data/fits/proton 2>&1 | tee score_proton_all_null_input.json.log
#echo "* PROTON TC"    & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_proton_tc.json             ~/astri_data/fits/proton 2>&1 | tee score_proton_tc.json.log
#echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_proton_${WT_LABEL_1}.json  ~/astri_data/fits/proton 2>&1 | tee score_proton_${WT_LABEL_1}.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done
#echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_proton_${WT_LABEL_2}.json  ~/astri_data/fits/proton 2>&1 | tee score_proton_${WT_LABEL_2}.json.log
#for FILE in .tmp*.fits ; do rm $FILE ; done

