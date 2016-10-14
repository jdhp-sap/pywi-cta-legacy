#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

# PROTON

./utils/simtel_to_fits_astri.py -o ~/astri_data/fits/proton/ ~/astri_data/proton/run10001.simtel.gz

# GAMMA

./utils/simtel_to_fits_astri.py -o ~/astri_data/fits/gamma/ ~/astri_data/gamma/run1001.simtel.gz

