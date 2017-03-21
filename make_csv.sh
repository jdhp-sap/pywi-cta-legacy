#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

NAME=2017_MM_DD

INPUT_DIR=./xps/${NAME}_sapcta
OUTPUT_FILE=./xps/${NAME}.csv

./utils/benchmark_json_to_flat_v2.py -o "${OUTPUT_FILE}" \
    ${INPUT_DIR}/score_*_ref.json \
    ${INPUT_DIR}/score_*_input.json \
    ${INPUT_DIR}/score_*_tc.json \
    ${INPUT_DIR}/score_*_WT-K-k-C1-m3-n4-s3.json \
    ${INPUT_DIR}/score_*_WT-K-k-C1-m3-n4-s2-2-3-3.json

