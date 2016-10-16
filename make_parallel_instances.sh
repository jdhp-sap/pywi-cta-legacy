#!/bin/sh

for INST_NUM in $(seq 24)
do
    echo ${INST_NUM}
    git clone https://github.com/jdhp-sap/sap-cta-data-pipeline.git ../sap-cta-data-pipeline_${INST_NUM}
done
