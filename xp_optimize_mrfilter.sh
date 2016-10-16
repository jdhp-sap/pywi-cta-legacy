#!/bin/bash

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=2000

PROTON_INPUT_FILES=$(find ~/astri_data/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
GAMMA_INPUT_FILES=$(find ~/astri_data/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})

# TAILCUT REF. ##########################

#TAILCUT_PARAMS="-T10 -t5"
#
#./datapipe/denoising/tailcut_jd.py -b mpdspd ${TAILCUT_PARAMS} -o score_proton_mpdspd_tailcut_jd.json ${PROTON_INPUT_FILES}
#./datapipe/denoising/tailcut_jd.py -b mpdspd ${TAILCUT_PARAMS} -o score_gamma_mpdspd_tailcut_jd.json  ${GAMMA_INPUT_FILES}

# WT REF. ###############################

#WT_MR_FILTER_PARAMS="-n4 -K -k -C1 -s3 -m3"
#
#./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_proton_mpdspd_wavelets_mrfilter_ref.json ${PROTON_INPUT_FILES}
#./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_gamma_mpdspd_wavelets_mrfilter_ref.json  ${GAMMA_INPUT_FILES}

# OPTIM #################################

NUM_SCALES_LIST=(3 4)
COEF_DETECT_METH_LIST=(1)
SIGMA_LIST=(2.5 2.75 3 3.25 3.5 3.75 4 4.25 4.5)
NOISE_MODEL_LIST=(1 2 3 5 6 7 8 9 10)

SUPPR_ISOLATED_PIX_LIST=("-k" "  ")
DETECT_ONLY_POS_STRUCT_LIST=("-p" "  ")
SUPPR_POS_CONST_LIST=("-P" "  ")

for NUM_SCALES in "${NUM_SCALES_LIST[@]}"
do

    for COEF_DETECT_METH in "${COEF_DETECT_METH_LIST[@]}"
    do

        for SIGMA in "${SIGMA_LIST[@]}"
        do

            for NOISE_MODEL in "${NOISE_MODEL_LIST[@]}"
            do

                for SUPPR_ISOLATED_PIX in "${SUPPR_ISOLATED_PIX_LIST[@]}"
                do

                    for DETECT_ONLY_POS_STRUCT in "${DETECT_ONLY_POS_STRUCT_LIST[@]}"
                    do

                        for SUPPR_POS_CONST in "${SUPPR_POS_CONST_LIST[@]}"
                        do

                            WT_MR_FILTER_PARAMS="-K -n${NUM_SCALES} -C${COEF_DETECT_METH} -s${SIGMA} -m${NOISE_MODEL} ${SUPPR_ISOLATED_PIX} ${DETECT_ONLY_POS_STRUCT} ${SUPPR_POS_CONST}"
                            OUTPUT_FILE_PARAMS=$(echo $WT_MR_FILTER_PARAMS | tr "-" "_" | tr -d '[[:space:]]')

                            echo "./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_proton_mpdspd_wavelets_mrfilter${OUTPUT_FILE_PARAMS}.json ..."
                            ./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_proton_mpdspd_wavelets_mrfilter${OUTPUT_FILE_PARAMS}.json ${PROTON_INPUT_FILES}

                            echo "./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_gamma_mpdspd_wavelets_mrfilter${OUTPUT_FILE_PARAMS}.json ..."
                            ./datapipe/denoising/wavelets_mrfilter.py -b mpdspd ${WT_MR_FILTER_PARAMS} -o score_gamma_mpdspd_wavelets_mrfilter${OUTPUT_FILE_PARAMS}.json ${GAMMA_INPUT_FILES}

                        done
                    done
                done
            done
        done
    done
done
