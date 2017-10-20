#!/bin/sh

cp $(find /home/jdecock/data/grid_prod3b_north/fits/lst/gamma/  -type f -name "*.fits" | head -n 10000) /dev/shm/.jd/fits/gamma/
cp $(find /home/jdecock/data/grid_prod3b_north/fits/lst/proton/ -type f -name "*.fits" | head -n 10000) /dev/shm/.jd/fits/proton/
