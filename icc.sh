#!/bin/bash

DIR="/home/comstock/images/icc/"
LIST=$DIR"icc_tiffs.txt"

find $DIR -name *.tif > $LIST

while read LINE
do
    exiftool -icc_profile -b -w icc $LINE
##
# NOTES
#
# If FNAME.icc exists, perform profile to profile conversion
#
# Else if FNAME.icc does not exist, embed sRGB profile

done<$LIST
