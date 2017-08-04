#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NUM_IMG=100

#TC_PARAMS="-T10 -t5 --kill-isolated-pixels"
#TC_PARAMS="-T10 -t5 --kill-isolated-pixels --geom ./datapipe/io/geom/gct.geom.json"
#TC_PARAMS="-T10 -t5 --kill-isolated-pixels --geom ./datapipe/io/geom/astri_cropped.geom.json"
TC_PARAMS="-T10 -t5 --kill-isolated-pixels --geom ./datapipe/io/geom/astri.geom.json"
#TC_PARAMS="-T10 -t5 --kill-isolated-pixels --geom ./datapipe/io/geom/flashcam2d.geom.json"

WT_NAN_NOISE_LAMBDA=0
WT_NAN_NOISE_MU=0
WT_NAN_NOISE_SIGMA=0

#WT_PARAMS_1="-K -k -C1 -m3 -n4 -s3       --kill-isolated-pixels --nan-noise-lambda=${WT_NAN_NOISE_LAMBDA} --nan-noise-mu=${WT_NAN_NOISE_MU} --nan-noise-sigma=${WT_NAN_NOISE_SIGMA}"
#WT_PARAMS_2="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --nan-noise-lambda=${WT_NAN_NOISE_LAMBDA} --nan-noise-mu=${WT_NAN_NOISE_MU} --nan-noise-sigma=${WT_NAN_NOISE_SIGMA}"
WT_PARAMS_1="-K -k -C1 -m3 -n4 -s3       --kill-isolated-pixels --nan-noise-lambda=${WT_NAN_NOISE_LAMBDA} --nan-noise-mu=${WT_NAN_NOISE_MU} --nan-noise-sigma=${WT_NAN_NOISE_SIGMA} --tmp-dir=/Volumes/ramdisk"
WT_PARAMS_2="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --nan-noise-lambda=${WT_NAN_NOISE_LAMBDA} --nan-noise-mu=${WT_NAN_NOISE_MU} --nan-noise-sigma=${WT_NAN_NOISE_SIGMA} --tmp-dir=/Volumes/ramdisk"

WT_LABEL_1="WT-K-k-C1-m3-n4-s3"
WT_LABEL_2="WT-K-k-C1-m3-n4-s2-2-3-3"

#MRFILTER_TMP_DIR="."
MRFILTER_TMP_DIR="/Volumes/ramdisk"



#GAMMA_FITS_DIR=~/astri_data/fits_cropped/gamma
#PROTON_FITS_DIR=~/astri_data/fits_cropped/proton

GAMMA_FITS_DIR=~/astri_data/fits/gamma
PROTON_FITS_DIR=~/astri_data/fits/proton

#GAMMA_FITS_DIR=/Volumes/ramdisk/astri_data/fits/gamma
#PROTON_FITS_DIR=/Volumes/ramdisk/astri_data/fits/proton

#PROTON_FITS_DIR=~/gct_data/fits/proton
#PROTON_FITS_DIR=~/gct_data/fits/proton/group1run100[0123].simtel.gz_TEL0*

#GAMMA_FITS_DIR=~/astri_data/fits_flashcam/gamma
#PROTON_FITS_DIR=~/astri_data/fits_flashcam/proton

#GAMMA_FITS_DIR=/Volumes/ramdisk/astri_data/fits_flashcam/gamma
#PROTON_FITS_DIR=/Volumes/ramdisk/astri_data/fits_flashcam/proton



####################
## GAMMAS ##########
####################
#
#echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_gamma_ref.json            $(find ${GAMMA_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_gamma_input.json          $(find ${GAMMA_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* GAMMA TC"     & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_gamma_tc.json             $(find ${GAMMA_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_gamma_${WT_LABEL_1}.json  $(find ${GAMMA_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
#echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_gamma_${WT_LABEL_2}.json  $(find ${GAMMA_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
#
####################
## PROTONS #########
####################
#
#echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_proton_ref.json            $(find ${PROTON_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_proton_input.json          $(find ${PROTON_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* PROTON TC"    & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_proton_tc.json             $(find ${PROTON_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_proton_${WT_LABEL_1}.json  $(find ${PROTON_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
#echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_proton_${WT_LABEL_2}.json  $(find ${PROTON_FITS_DIR} -type f -name "*.fits" | head -n ${NUM_IMG})
#for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done

###################
# ALL GAMMAS ######
###################

echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_gamma_ref.json            ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_ref.json.log
echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_gamma_input.json          ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_input.json.log
echo "* GAMMA TC"     & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_gamma_tc.json             ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_tc.json.log
echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_gamma_${WT_LABEL_1}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_LABEL_1}.json.log
for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
echo "* GAMMA WT"     & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_gamma_${WT_LABEL_2}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_LABEL_2}.json.log
for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done

#####################
## ALL PROTONS ######
#####################

echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py          -b all --label="Ref"                          -o score_proton_ref.json            ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_ref.json.log
echo "* NULL (INPUT)" & ./datapipe/denoising/null.py              -b all --label="Input"                        -o score_proton_input.json          ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_input.json.log
echo "* PROTON TC"    & ./datapipe/denoising/tailcut.py           -b all --label="Tailcut-5-10"  ${TC_PARAMS}   -o score_proton_tc.json             ${PROTON_FITS_DIR} 2>&1 | tee score_proton_tc.json.log
echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_1}" ${WT_PARAMS_1} -o score_proton_${WT_LABEL_1}.json  ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_LABEL_1}.json.log
for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
echo "* PROTON WT"    & ./datapipe/denoising/wavelets_mrfilter.py -b all --label="${WT_LABEL_2}" ${WT_PARAMS_2} -o score_proton_${WT_LABEL_2}.json  ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_LABEL_2}.json.log
for FILE in ${MRFILTER_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done

