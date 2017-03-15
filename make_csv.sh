#!/bin/sh

./utils/benchmark_json_to_flat_v2.py -o xps/best.csv \
    xps/2017_03_15/score_*_ref.json \
    xps/2017_03_15/score_*_input.json \
    xps/2017_03_15/score_*_tc.json \
    xps/2017_03_15/score_*_WT-K-k-C1-m3-n4-s3.json \
    xps/2017_03_15/score_*_WT-K-k-C1-m3-n4-s2-2-3-3.json
