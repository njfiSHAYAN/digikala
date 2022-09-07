#!/bin/bash
changes=$1
appChanged=$(echo "$changes" | grep application)
echo $appChanged
if [ -n $appChanged ]; then
    echo "1"
else
    echo "0"
fi