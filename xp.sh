#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

NUM_IMG=10000

# PROTONS #########

echo "" # & echo "* PROTON MPD NULL"        & ./datapipe/denoising/null.py              -b mpd                            -o score_proton_mpd_null.json                  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* PROTON MPD FFT"         & ./datapipe/denoising/fft.py               -b mpd    -s -t0.004            t -o score_proton_mpd_fft.json                   $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* PROTON MPD TAILCUT"     & ./datapipe/denoising/tailcut_jd.py        -b mpd    -T0.75 -t0.5          t -o score_proton_mpd_tailcut_jd.json            $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* PROTON MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrfilter.py -b mpd                          t -o score_proton_mpd_wavelets_mrfilter.json     $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo ""   & echo "* PROTON MPDSDP NULL"     & ./datapipe/denoising/null.py              -b mpdspd                         -o score_proton_mpdspd_null.json               $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON MPDSDP FFT"      & ./datapipe/denoising/fft.py               -b mpdspd -s -t0.004              -o score_proton_mpdspd_fft.json                $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b mpdspd -T0.75 -t0.5            -o score_proton_mpdspd_tailcut_jd.json         $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b mpdspd                         -o score_proton_mpdspd_wavelets_mrfilter.json  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo ""   & echo "* PROTON SSPD NULL"       & ./datapipe/denoising/null.py              -b sspd                           -o score_proton_sspd_null.json                 $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON SSPD FFT"        & ./datapipe/denoising/fft.py               -b sspd   -s -t0.004              -o score_proton_sspd_fft.json                  $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON SSPD TAILCUT"    & ./datapipe/denoising/tailcut_jd.py        -b sspd   -T0.75 -t0.5            -o score_proton_sspd_tailcut_jd.json           $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo ""   & echo "* PROTON SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrfilter.py -b sspd                           -o score_proton_sspd_wavelets_mrfilter.json    $(find ~/data/astri_mini_array/fits/proton -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

#mkdir proton_cleaned_images
#echo ""   & for FILE in *.pdf ; do mv "$FILE" ./proton_cleaned_images  ; done


# GAMMAS ##########

echo "" # & echo "* GAMMA MPD NULL"        & ./datapipe/denoising/null.py              -b mpd                            -o score_gamma_mpd_null.json                   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPD FFT"         & ./datapipe/denoising/fft.py               -b mpd    -s -t0.004   -          -o score_gamma_mpd_fft.json                    $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPD TAILCUT"     & ./datapipe/denoising/tailcut_jd.py        -b mpd    -T0.75 -t0.5 -          -o score_gamma_mpd_tailcut_jd.json             $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrfilter.py -b mpd                 -          -o score_gamma_mpd_wavelets_mrfilter.json      $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo "" # & echo "* GAMMA MPDSDP NULL"     & ./datapipe/denoising/null.py              -b mpdspd                         -o score_gamma_mpdspd_null.json                $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPDSDP FFT"      & ./datapipe/denoising/fft.py               -b mpdspd -s -t0.004              -o score_gamma_mpdspd_fft.json                 $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b mpdspd -T0.75 -t0.5            -o score_gamma_mpdspd_tailcut_jd.json          $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b mpdspd                         -o score_gamma_mpdspd_wavelets_mrfilter.json   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo "" # & echo "* GAMMA SSPD NULL"       & ./datapipe/denoising/null.py              -b sspd                           -o score_gamma_sspd_null.json                  $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA SSPD FFT"        & ./datapipe/denoising/fft.py               -b sspd   -s -t0.004              -o score_gamma_sspd_fft.json                   $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA SSPD TAILCUT"    & ./datapipe/denoising/tailcut_jd.py        -b sspd   -T0.75 -t0.5            -o score_gamma_sspd_tailcut_jd.json            $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & echo "* GAMMA SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrfilter.py -b sspd                           -o score_gamma_sspd_wavelets_mrfilter.json     $(find ~/data/astri_mini_array/fits/gamma -type f -name "*.fits" | head -n ${NUM_IMG})
echo "" # & for FILE in *.fits ; do rm $FILE ; done

# ALL GAMMAS ######

echo "" # & echo "* GAMMA MPD NULL"        & ./datapipe/denoising/null.py              -b mpd                            -o score_gamma_mpd_null.json                   ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* GAMMA MPD FFT"         & ./datapipe/denoising/fft.py               -b mpd -s -t0.004      -          -o score_gamma_mpd_fft.json                    ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* GAMMA MPD TAILCUT"     & ./datapipe/denoising/tailcut_jd.py        -b mpd -T0.75 -t0.5    -          -o score_gamma_mpd_tailcut_jd.json             ~/data/astri_mini_array/fits/gamma
echo "" # & echo "* GAMMA MPD WAVELETS"    & ./datapipe/denoising/wavelets_mrfilter.py -b mpd                 -          -o score_gamma_mpd_wavelets_mrfilter.json      ~/data/astri_mini_array/fits/gamma
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo ""   & echo "* GAMMA MPDSDP NULL"     & ./datapipe/denoising/null.py              -b mpdspd                         -o score_gamma_mpdspd_null.json                ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA MPDSDP FFT"      & ./datapipe/denoising/fft.py               -b mpdspd -s -t0.004              -o score_gamma_mpdspd_fft.json                 ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA MPDSDP TAILCUT"  & ./datapipe/denoising/tailcut_jd.py        -b mpdspd -T0.75 -t0.5            -o score_gamma_mpdspd_tailcut_jd.json          ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA MPDSDP WAVELETS" & ./datapipe/denoising/wavelets_mrfilter.py -b mpdspd                         -o score_gamma_mpdspd_wavelets_mrfilter.json   ~/data/astri_mini_array/fits/gamma
echo "" # & for FILE in *.fits ; do rm $FILE ; done

echo ""   & echo "* GAMMA SSPD NULL"       & ./datapipe/denoising/null.py              -b sspd                           -o score_gamma_sspd_null.json                  ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA SSPD FFT"        & ./datapipe/denoising/fft.py               -b sspd -s -t0.004                -o score_gamma_sspd_fft.json                   ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA SSPD TAILCUT"    & ./datapipe/denoising/tailcut_jd.py        -b sspd -T0.75 -t0.5              -o score_gamma_sspd_tailcut_jd.json            ~/data/astri_mini_array/fits/gamma
echo ""   & echo "* GAMMA SSPD WAVELETS"   & ./datapipe/denoising/wavelets_mrfilter.py -b sspd                           -o score_gamma_sspd_wavelets_mrfilter.json     ~/data/astri_mini_array/fits/gamma
echo "" # & for FILE in *.fits ; do rm $FILE ; done

#mkdir gamma_cleaned_images
#echo ""   & for FILE in *.pdf ; do mv "$FILE" ./gamma_cleaned_images  ; done

