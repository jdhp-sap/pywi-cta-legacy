#!/bin/sh

MACPORTSPYTHONPATH=/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python35.zip:/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5:/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/plat-darwin:/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/lib-dynload:/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages
ANACONDAPYTHONPATH=/Users/jdecock/anaconda/lib/python35.zip:/Users/jdecock/anaconda/lib/python3.5:/Users/jdecock/anaconda/lib/python3.5/plat-darwin:/Users/jdecock/anaconda/lib/python3.5/lib-dynload:/Users/jdecock/anaconda/lib/python3.5/site-packages:/Users/jdecock/anaconda/lib/python3.5/site-packages/Sphinx-1.4.6-py3.5.egg:/Users/jdecock/anaconda/lib/python3.5/site-packages/aeosa:/Users/jdecock/anaconda/lib/python3.5/site-packages/pydfm-3.0.dev3-py3.5.egg:/Users/jdecock/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg

# Run with MacPorts ###########################################################

#export PYTHONPATH=../../:$PYTHONPATH
#export PYTHONPATH=.:$PYTHONPATH
#
#/opt/local/bin/python3.5 ./benchmark/benchmark.py $1

# Run with Anaconda ###########################################################

#export PYTHONPATH=/opt/local/lib/girepository-1.0:$PYTHONPATH
#export PYTHONPATH=/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/gi:$PYTHONPATH

# Workaround:
# - GTK3 only works with MacPorts Python version (GTK3 is not available in Anaconda)
# - Ctapipe only works with Anaconda Python version
# Thus:
# - Set both paths but give Anaconda a higher priority

export PYTHONPATH=$MACPORTSPYTHONPATH:$PYTHONPATH
export PYTHONPATH=$ANACONDAPYTHONPATH:$PYTHONPATH

export PYTHONPATH=../../:$PYTHONPATH
export PYTHONPATH=.:$PYTHONPATH

python3 ./benchmark/benchmark.py $1
