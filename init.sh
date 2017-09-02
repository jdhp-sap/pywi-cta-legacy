#!/bin/sh

source activate cta

if [ -d /Volumes ]
then
    # Mac OS
    export PYTHONPATH=.:$PYTHONPATH ;
elif [ -d /proc ]
then
    # Linux
    export PYTHONPATH=.:~/git/pub/ext/ctapipe-extra:$PYTHONPATH ;
else
    echo "Unknown system"
    exit 1
fi
