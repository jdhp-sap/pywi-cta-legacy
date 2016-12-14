#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

OUT_DIR=../../jdhp-sap-docs/cta_data_pipeline_report_2016_12_14/figs

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/tc_vs_wt_ref_eshape.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_ref.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/tc_vs_wt_ref_eenergy.png --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_ref.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/tc_vs_wt_ref_theta.png   --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_ref.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/tc_vs_wt_ref_theta2.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_ref.json

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/wt_ref_vs_wt_c2_eshape.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/wt_ref_vs_wt_c2_eenergy.png --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/wt_ref_vs_wt_c2_theta.png   --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/wt_ref_vs_wt_c2_theta2.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2.json

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/tc_vs_wt_c2_eshape.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/tc_vs_wt_c2_eenergy.png --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/tc_vs_wt_c2_theta.png   --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_c2.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/tc_vs_wt_c2_theta2.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_c2.json

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/wt_ref_vs_wt_kill_eshape.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/wt_ref_vs_wt_kill_eenergy.png --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/wt_ref_vs_wt_kill_theta.png   --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/wt_ref_vs_wt_kill_theta2.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_kill.json

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/wt_ref_vs_wt_c2_kill_eshape.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/wt_ref_vs_wt_c2_kill_eenergy.png --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/wt_ref_vs_wt_c2_kill_theta.png   --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/wt_ref_vs_wt_c2_kill_theta2.png  --logy score_gamma_all_wavelets_mrfilter_ref.json  score_gamma_all_wavelets_mrfilter_c2_kill.json

#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_shape      --title "$\mathcal{E}_{shape}$"  -o ${OUT_DIR}/tc_vs_wt_kill_eshape.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m e_energy     --title "$\mathcal{E}_{energy}$" -o ${OUT_DIR}/tc_vs_wt_kill_eenergy.png --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta"                  -o ${OUT_DIR}/tc_vs_wt_kill_theta.png   --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
#./utils/plot_score_histogram_by_decades_of_energy.py --quiet -m hillas_theta --title "Theta 2 (kill on ref.)" -o ${OUT_DIR}/tc_vs_wt_kill_theta2.png  --logy score_gamma_all_tailcut_ref.json  score_gamma_all_wavelets_mrfilter_kill.json
