#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

echo
echo
echo "TEST_BENCHMARK_ASSESS"
./tests/test_benchmark_assess.py

echo
echo
echo "TEST_DENOISING_TAILCUT"
./tests/test_denoising_tailcut.py

echo
echo
echo "TEST_IO_IMAGES"
./tests/test_io_images.py

