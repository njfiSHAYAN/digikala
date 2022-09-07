#!/bin/bash
changes=$1
deployChange=$(echo "$changes" | grep -e "helmCharts|ansible")
if [ ${#deployChange} -gt 0 ]; then
    echo "1"
else
    echo "0"
fi