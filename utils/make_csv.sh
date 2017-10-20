#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH
source activate cta

INPUT_DIR="$1"
OUTPUT_FILE="$2"

./utils/benchmark_json_to_flat_v2.py -o "${OUTPUT_FILE}" \
    ${INPUT_DIR}/score_*_ref.json \
    ${INPUT_DIR}/score_*_input.json \
    ${INPUT_DIR}/score_*_tc.json \
    ${INPUT_DIR}/score_*_WT*.json

