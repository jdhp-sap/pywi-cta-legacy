#!/bin/sh

. ./utils/init.sh

# SETUP #######################################################################

NUM_IMG=15000
#NUM_IMG=100

# INSTRUMENT ##########################

#INST="astri_mini_inaf"
#INST="astri_mini_konrad"
#INST="gct_mini_konrad"
#INST="digicam_mini_konrad"

#INST="flashcam_mini_inaf"
#INST="nectarcam_grid_prod3b_north"

INST="lstcam_grid_prod3b_north"

###############################################################################
###############################################################################
###############################################################################

echo "NUM_IMG: ${NUM_IMG}"
echo "INST: ${INST}"

# SYSTEM ##############################

if [ -d /Volumes ]
then
    SYS_NAME="macos"
elif [ -d /proc ]
then
    SYS_NAME="linux"
else
    echo "Unknown system"
    exit 1
fi

echo "SYS_NAME: ${SYS_NAME}"

case ${SYS_NAME} in
macos)
    export PYTHONPATH=.:$PYTHONPATH ;
    if [ -d /Volumes/ramdisk ]
    then
        MR_TMP_DIR="/Volumes/ramdisk"
    else
        MR_TMP_DIR="."
        echo "*** WARNING: CANNOT USE RAMDISK FOR TEMPORARY FILES ; USE ./ INSTEAD... ***"
    fi
    ;;
linux)
    export PYTHONPATH=.:~/git/pub/ext/ctapipe-extra:$PYTHONPATH ;
    if [ -d /dev/shm/.jd ]
    then
        MR_TMP_DIR="/dev/shm/.jd"
    else
        MR_TMP_DIR="."
        echo "*** WARNING: CANNOT USE RAMDISK FOR TEMPORARY FILES ; USE ./ INSTEAD... ***"
    fi
    ;;
*)
    echo "Unknown system" ;
    exit 1
    ;;
esac

echo "MR_TMP_DIR: ${MR_TMP_DIR}"

# DENOISING PARAMETERS AND INPUT FILES ########################################

# TODO
#GAMMA_FITS_DIR=${MR_TMP_DIR}/astri_data/fits/gamma
#PROTON_FITS_DIR=${MR_TMP_DIR}/astri_data/fits/proton

# TODO
#GAMMA_FITS_DIR=${MR_TMP_DIR}/astri_data/fits_flashcam/gamma
#PROTON_FITS_DIR=${MR_TMP_DIR}/astri_data/fits_flashcam/proton

case ${INST} in
astri_mini_inaf)
    CAM_ID="ASTRICam"

    GAMMA_FITS_DIR=~/data/astri_mini_array/fits/astri/gamma ;
    PROTON_FITS_DIR=~/data/astri_mini_array/fits/astri/proton ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/astri_inaf_cdf_gamma.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="7" ; # Tino
    #TC_LTH="5" ; # Tino
    #TC_LABEL="Tailcut-Tino-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="7" ;   # CTA Abelardo 2nd pass
    TC_LTH="3.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2016
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3       --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3"

    ## 2017/02 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s1,1,2,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s1-1-2-1" ;
    ;;
astri_mini_konrad)
    CAM_ID="ASTRICam"

    #GAMMA_FITS_DIR=~/data/astri_mini_array_konrad/fits/astri_v2/gamma ;
    #PROTON_FITS_DIR=~/data/astri_mini_array_konrad/fits/astri_v2/proton ;
    GAMMA_FITS_DIR=~/data/astri_mini_array_konrad/simtel/astri_v2/gamma/ ;
    PROTON_FITS_DIR=~/data/astri_mini_array_konrad/simtel/astri_v2/proton/ ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/astri_konrad_cdf_gamma.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="7" ; # Tino
    #TC_LTH="5" ; # Tino
    #TC_LABEL="Tailcut-Tino-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="7" ;   # CTA Abelardo 2nd pass
    TC_LTH="3.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2017/02 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,1,3.5,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-1-3.5-1" ;
    ;;
gct_mini_konrad)
    CAM_ID="CHEC"

    #GAMMA_FITS_DIR=~/data/gct_mini_array_konrad/fits/gct/gamma ;
    #PROTON_FITS_DIR=~/data/gct_mini_array_konrad/fits/gct/proton ;
    GAMMA_FITS_DIR=~/data/gct_mini_array_konrad/simtel/gct/gamma/ ;
    PROTON_FITS_DIR=~/data/gct_mini_array_konrad/simtel/gct/proton/ ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/gct_konrad_cdf_gamma.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ; # CTA Abelardo 1st pass
    #TC_LTH="2" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="2" ; # CTA Abelardo 2nd pass
    TC_LTH="1" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2,3,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2-3-3" ;
    ;;
digicam_mini_konrad)
    CAM_ID="DigiCam"

    GAMMA_FITS_DIR=~/data/sst1m_mini_array_konrad/fits/sst1m/gamma ;
    PROTON_FITS_DIR=~/data/sst1m_mini_array_konrad/fits/sst1m/proton ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/digicam_konrad_cdf_gamma.json ;

    #TC_HTH="10" ;  # HESS
    #TC_LTH="5" ;   # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="6" ;   # CTA Abelardo 1st pass
    #TC_LTH="3" ;   # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="3" ;   # CTA Abelardo 2nd pass
    #TC_LTH="1.5" ; # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="4" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LTH="1" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LABEL="Tailcut-BF1-${TC_HTH}-${TC_LTH}" ;

    ## 2017/09/11 (BF res1) (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,3,4,4 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-3-4-4" ;

    # 2017/10/24 (SAES)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s6.274,2.629,7.755,0.076 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s6.274-2.629-7.755-0.076" ;
    ;;
flashcam_mini_inaf)
    CAM_ID="FlashCam"

    GAMMA_FITS_DIR=~/data/astri_mini_array/fits/flashcam/gamma ;
    PROTON_FITS_DIR=~/data/astri_mini_array/fits/flashcam/proton ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/flashcam_grid_prod3b_north_cdf_gamma.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="8" ; # CTA Abelardo 1st pass
    #TC_LTH="4" ; # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="5" ;   # CTA Abelardo 2nd pass
    TC_LTH="2.5" ; # CTA Abelardo 2nd pass
    TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    ## 2017/07 (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s4,4,5,4 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s4-4-5-4" ;

    # 2017/09/07 (BF res0.5)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s4.5,4.5,4.5,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s4.5-4.5-4.5-1" ;
    ;;
nectarcam_grid_prod3b_north)
    CAM_ID="NectarCam"

    GAMMA_FITS_DIR=~/data/grid_prod3b_north/fits/nectarcam/gamma ;
    PROTON_FITS_DIR=~/data/grid_prod3b_north/fits/nectarcam/proton ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/nectarcam_grid_prod3b_north_cdf_gamma.json ;

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="8" ;  # CTA Abelardo 1st pass
    #TC_LTH="4" ;  # CTA Abelardo 1st pass
    #TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ;  # CTA Abelardo 2nd pass
    #TC_LTH="2" ;  # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="5" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LTH="1" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    TC_LABEL="Tailcut-BF1-${TC_HTH}-${TC_LTH}" ;

    ## 2017/08
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,4.5,3.5,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-4.5-3.5-3" ;

    ## 2017/09/07 (BF res0.5) (presented in LaPalma CTA meeting 2017-11-05)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s3,2.5,4,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s3-2.5-4-1" ;

    # 2017/10/24 (SAES)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s13.013,2.549,6.559,1.412 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s13.013-2.549-6.559-1.412" ;
    ;;
lstcam_grid_prod3b_north)
    CAM_ID="LSTCam"

    GAMMA_FITS_DIR=~/data/grid_prod3b_north/fits/lst/gamma ;
    PROTON_FITS_DIR=~/data/grid_prod3b_north/fits/lst/proton ;
    #GAMMA_FITS_DIR=~/data/grid_prod3b_north/simtel/gamma ;
    #PROTON_FITS_DIR=~/data/grid_prod3b_north/simtel/proton ;

    WT_NAN_NOISE_CDF_FILE=./datapipe/denoising/cdf/lstcam_grid_prod3b_north_cdf_gamma.json ;

    # TAILCUT #################################################################

    #TC_HTH="10" ; # HESS
    #TC_LTH="5" ;  # HESS
    #TC_LABEL="Tailcut-HESS-${TC_HTH}-${TC_LTH}" ;

    TC_HTH="6" ; # CTA Abelardo 1st pass
    TC_LTH="3" ; # CTA Abelardo 1st pass
    TC_LABEL="Tailcut-CTA1-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ; # CTA Abelardo 2nd pass
    #TC_LTH="2" ; # CTA Abelardo 2nd pass
    #TC_LABEL="Tailcut-CTA2-${TC_HTH}-${TC_LTH}" ;

    #TC_HTH="4" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    #TC_LTH="1" ;   # 2018/01/09 Brutforce Delta psi optim (res 1.0, 1000 img, mean, 30-2000 PE, missing img penalty: 90)
    #TC_LABEL="Tailcut-BF1-${TC_HTH}-${TC_LTH}" ;

    # MR_FILTER ###############################################################

    # 2017/08 (presented in LaPalma CTA meeting 2017-11-05)
    WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,4.5,3.5,3 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-4.5-3.5-3" ;

    ## 2017/09/07 (BF res0.5)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s2,2.5,4,1 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s2-2.5-4-1" ;

    ## 2017/10/24 (SAES)
    #WT_MRF_PARAMS="-K -k -C1 -m3 -n4 -s23.343,2.490,-2.856,-0.719 --kill-isolated-pixels --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    #WT_MRF_LABEL="WT-K-k-C1-m3-n4-s23.343-2.490--2.856--0.719" ;

    # MR_TRANSFORM ############################################################

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 23.7,3.25,1. -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_23.7_3.25_1._-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 15.,2.,1. -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_15._2._1._-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 13.,1.5 -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_13._1.5_-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 13.,1.3 -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_13._1.3_-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 10.,1.3 -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_10._1.3_-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f hard_filtering -t 7.5,1.3 -L mask -p --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_hard_filtering_-t_7.5_1.3_-L_mask_-p" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 15.,2.,1. -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_15._2._1._-L_mask" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 13.,1.5 -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_13._1.5_-L_mask" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 13.,1.3 -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_13._1.3_-L_mask" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 10.,1.3 -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_10._1.3_-L_mask" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 7.5,1.3 -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_7.5_1.3_-L_mask" ;

    # 2017/02/14
    WT_MRT_PARAMS="-f common_hard_filtering -t 11.,1.8,0.7 -L mask --noise-cdf-file=${WT_NAN_NOISE_CDF_FILE} --tmp-dir=${MR_TMP_DIR}" ;
    WT_MRT_LABEL="WT_MRT_-f_common_hard_filtering_-t_11._1.8_0.7_-L_mask" ;
    ;;
*)
    echo "Unknown option" ;
    exit 1
    ;;
esac

TC_PARAMS="-T${TC_HTH} -t${TC_LTH} --kill-isolated-pixels" ;

echo "TC_PARAMS: ${TC_PARAMS}"
echo "TC_LABEL:  ${TC_LABEL}"
echo "WT_MRF_PARAMS: ${WT_MRF_PARAMS}"
echo "WT_MRF_LABEL:  ${WT_MRF_LABEL}"
echo "WT_MRT_PARAMS: ${WT_MRT_PARAMS}"
echo "WT_MRT_LABEL:  ${WT_MRT_LABEL}"

echo "GAMMA_FITS_DIR:  ${GAMMA_FITS_DIR}"
echo "PROTON_FITS_DIR: ${PROTON_FITS_DIR}"

echo "WT_NAN_NOISE_CDF_FILE: ${WT_NAN_NOISE_CDF_FILE}"

if [ ! -d "${GAMMA_FITS_DIR}" ]
then
    echo "*** WARNING: CANNOT READ ${GAMMA_FITS_DIR} ***"
    exit 1
fi

if [ ! -d "${PROTON_FITS_DIR}" ]
then
    echo "*** WARNING: CANNOT READ ${PROTON_FITS_DIR} ***"
    exit 1
fi

# RUN DENOISING ###############################################################

sleep 5

###################
# ALL GAMMAS ######
###################

echo "* NULL (REF.)"  & ./datapipe/denoising/null_ref.py             -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Ref"                      -o score_gamma_ref.json          ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_ref.json.log ;
echo "* NULL (INPUT)" & ./datapipe/denoising/null.py                 -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Input"                    -o score_gamma_input.json        ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_all_null_input.json.log ;
echo "* GAMMA TC"     & ./datapipe/denoising/tailcut.py              -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${TC_LABEL}" ${TC_PARAMS} -o score_gamma_${TC_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${TC_LABEL}.json.log ;
echo "* GAMMA WT MRF" & ./datapipe/denoising/wavelets_mrfilter.py    -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRF_LABEL}" ${WT_MRF_PARAMS} -o score_gamma_${WT_MRF_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_MRF_LABEL}.json.log ;
for FILE in ${MR_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
echo "* GAMMA WT MRT" & ./datapipe/denoising/wavelets_mrtransform.py -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRT_LABEL}" ${WT_MRT_PARAMS} -o score_gamma_${WT_MRT_LABEL}.json  ${GAMMA_FITS_DIR} 2>&1 | tee score_gamma_${WT_MRT_LABEL}.json.log ;
for FILE in ${MR_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done

#####################
## ALL PROTONS ######
#####################

echo "* NULL (REF.)"   & ./datapipe/denoising/null_ref.py             -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Ref"                      -o score_proton_ref.json         ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_ref.json.log ;
echo "* NULL (INPUT)"  & ./datapipe/denoising/null.py                 -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="Input"                    -o score_proton_input.json       ${PROTON_FITS_DIR} 2>&1 | tee score_proton_all_null_input.json.log ;
echo "* PROTON TC"     & ./datapipe/denoising/tailcut.py              -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${TC_LABEL}" ${TC_PARAMS} -o score_proton_${TC_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${TC_LABEL}.json.log ;
echo "* PROTON WT MRF" & ./datapipe/denoising/wavelets_mrfilter.py    -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRF_LABEL}" ${WT_MRF_PARAMS} -o score_proton_${WT_MRF_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_MRF_LABEL}.json.log ;
for FILE in ${MR_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
echo "* PROTON WT MRT" & ./datapipe/denoising/wavelets_mrtransform.py -b all --max-images ${NUM_IMG} --camid ${CAM_ID} --label="${WT_MRT_LABEL}" ${WT_MRT_PARAMS} -o score_proton_${WT_MRT_LABEL}.json ${PROTON_FITS_DIR} 2>&1 | tee score_proton_${WT_MRT_LABEL}.json.log ;
for FILE in ${MR_TMP_DIR}/.tmp*.fits ; do rm $FILE ; done
