#!/bin/sh

OUTPUT_DIR=./xps/2017_MM_DD_sapcta/

mkdir "${OUTPUT_DIR}"

# See: http://stackoverflow.com/questions/1228466/how-to-filter-files-when-using-scp-to-copy-dir-recursively
rsync  -e ssh -rav --exclude='*/.git/' --exclude='*/utils/' --exclude='*/tests/' --exclude='*/docs/' --exclude='*/datapipe/' --include '*/' --include='*.json' --exclude='*'     sapcta:/home/jdecock/xp/ "${OUTPUT_DIR}"
rsync  -e ssh -rav --exclude='*/.git/' --exclude='*/utils/' --exclude='*/tests/' --exclude='*/docs/' --exclude='*/datapipe/' --include '*/' --include='*.json.log' --exclude='*' sapcta:/home/jdecock/xp/ "${OUTPUT_DIR}"

# Remove empty directories
mv    ${OUTPUT_DIR}/run*/*.json* ${OUTPUT_DIR}/
rmdir ${OUTPUT_DIR}/run*/*
rmdir ${OUTPUT_DIR}/run*
