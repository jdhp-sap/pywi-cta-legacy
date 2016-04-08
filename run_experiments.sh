#!/bin/sh

INFILE=CT062.fits

./denoising_with_fft.py -s -t 0.02 "${INFILE}"
./denoising_with_wavelets_mr_transform.py "${INFILE}"
