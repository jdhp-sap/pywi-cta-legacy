#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

INDEX=10

# GAMMA

./datapipe/denoising/fft.py                -s -t0.004    --saveplot gamma_e1_fft_bad.pdf       "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_gamma_mpdspd_fft.json                2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot gamma_e1_tailcut_bad.pdf   "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_gamma_mpdspd_tailcut.json            2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot gamma_e1_wt_bad.pdf        "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_gamma_mpdspd_wavelets_mrfilter.json  2>/dev/null | awk '{print $1}' | head -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot gamma_e1_fft_good.pdf      "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_gamma_mpdspd_fft.json                2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot gamma_e1_tailcut_good.pdf  "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_gamma_mpdspd_tailcut.json            2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot gamma_e1_wt_good.pdf       "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_gamma_mpdspd_wavelets_mrfilter.json  2>/dev/null | awk '{print $1}' | tail -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot gamma_e2_fft_bad.pdf       "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_gamma_mpdspd_fft.json                2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot gamma_e2_tailcut_bad.pdf   "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_gamma_mpdspd_tailcut.json            2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot gamma_e2_wt_bad.pdf        "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_gamma_mpdspd_wavelets_mrfilter.json  2>/dev/null | awk '{print $1}' | head -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot gamma_e2_fft_good.pdf      "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_gamma_mpdspd_fft.json                2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot gamma_e2_tailcut_good.pdf  "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_gamma_mpdspd_tailcut.json            2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot gamma_e2_wt_good.pdf       "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_gamma_mpdspd_wavelets_mrfilter.json  2>/dev/null | awk '{print $1}' | tail -n 1)"

# PROTON

./datapipe/denoising/fft.py                -s -t0.004    --saveplot proton_e1_fft_bad.pdf      "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_proton_mpdspd_fft.json               2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot proton_e1_tailcut_bad.pdf  "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_proton_mpdspd_tailcut.json           2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot proton_e1_wt_bad.pdf       "$(./utils/search_input_by_score_range.py --worst $INDEX --index 0 score_proton_mpdspd_wavelets_mrfilter.json 2>/dev/null | awk '{print $1}' | head -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot proton_e1_fft_good.pdf     "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_proton_mpdspd_fft.json               2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot proton_e1_tailcut_good.pdf "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_proton_mpdspd_tailcut.json           2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot proton_e1_wt_good.pdf      "$(./utils/search_input_by_score_range.py --best  $INDEX --index 0 score_proton_mpdspd_wavelets_mrfilter.json 2>/dev/null | awk '{print $1}' | tail -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot proton_e2_fft_bad.pdf      "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_proton_mpdspd_fft.json               2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot proton_e2_tailcut_bad.pdf  "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_proton_mpdspd_tailcut.json           2>/dev/null | awk '{print $1}' | head -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot proton_e2_wt_bad.pdf       "$(./utils/search_input_by_score_range.py --worst $INDEX --index 1 score_proton_mpdspd_wavelets_mrfilter.json 2>/dev/null | awk '{print $1}' | head -n 1)"

./datapipe/denoising/fft.py                -s -t0.004    --saveplot proton_e2_fft_good.pdf     "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_proton_mpdspd_fft.json               2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/tailcut.py            -T0.75 -t0.5  --saveplot proton_e2_tailcut_good.pdf "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_proton_mpdspd_tailcut.json           2>/dev/null | awk '{print $1}' | tail -n 1)"
./datapipe/denoising/wavelets_mrfilter.py                --saveplot proton_e2_wt_good.pdf      "$(./utils/search_input_by_score_range.py --best  $INDEX --index 1 score_proton_mpdspd_wavelets_mrfilter.json 2>/dev/null | awk '{print $1}' | tail -n 1)"

