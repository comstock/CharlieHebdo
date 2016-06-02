#!/bin/bash

DIR="/home/comstock/images/icc/"
LIST=$DIR"icc_tiffs.txt"

find $DIR -name *.tif > $LIST

while read LINE
do
    exiftool -icc_profile -b -w icc $LINE
    ICCFILENAME=`sed 's/tif$/icc$/' $LINE`
    if [ -e $ICCFILENAME ]; then
	echo "WORKS"
    else
	echo "NOPE"
    fi
    echo "ICC FNAME : "$ICCFILENAME
done < $LIST
