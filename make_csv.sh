#!/bin/sh

# xps/2017_02_22_sapcta/run_1/score_*_all_null_ref.json                   Ref.
# xps/2017_02_22_sapcta/run_1/score_*_all_null_input.json                 Input
# xps/2017_02_22_sapcta/run_1/score_*_all_tailcut_kill.json               Tailcut
# xps/2017_03_03/score_*_all_wavelets_mrfilter_ref.json                   WT-ref
# xps/2017_02_22_sapcta/run_1/score_*_all_wavelets_mrfilter_kill.json     WT-ref-f3-s3
# xps/2017_02_22_sapcta/run_2/score_*_all_wavelets_mrfilter_jl13.json     WT-t24-f3-s4
# xps/2017_02_22_sapcta/run_3/score_*_all_wavelets_mrfilter_jl23.json     WT-t28-f3-s5
# xps/2017_02_23_sapcta/run_8/score_*_all_wavelets_mrfilter_kill.json     WT-ref-s2-2-3-3

./utils/benchmark_json_to_flat_v2.py -o xps/best.csv \
    xps/2017_02_22_sapcta/run_1/score_*_all_null_ref.json \
    xps/2017_02_22_sapcta/run_1/score_*_all_null_input.json \
    xps/2017_02_22_sapcta/run_1/score_*_all_tailcut_kill.json \
    \
    xps/2017_03_03/score_*_all_wavelets_mrfilter_ref.json \
    \
    xps/2017_02_22_sapcta/run_1/score_*_all_wavelets_mrfilter_kill.json \
    xps/2017_02_22_sapcta/run_2/score_*_all_wavelets_mrfilter_jl13.json \
    xps/2017_02_22_sapcta/run_3/score_*_all_wavelets_mrfilter_jl23.json \
    xps/2017_02_23_sapcta/run_8/score_*_all_wavelets_mrfilter_kill.json

