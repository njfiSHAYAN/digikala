#!/bin/bash
changes=$1
appChanged=$(echo "$changes" | tr '\n' '-' | grep application)
if [ ${#appChanged} -gt 0 ]; then
    echo "1"
else
    echo "0"
fi
