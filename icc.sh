#!/bin/bash

DIR="/home/comstock/images/icc/"
LIST=$DIR"icc_tiffs.txt"

find $DIR -name *.tif > $LIST
#cat  $LIST
EXIFOUTPUT=$DIR"exifoutput.txt"

while read LINE
do
    exiftool $LINE | grep "Profile Description" > $EXIFOUTPUT
    if [ ! -z $EXIFOUTPUT ]
	then echo "No Profile in "$LINE
    elif [! -n $EXIFOUTPUT ]
	then echo $LINE $EXIFOUTPUT
    fi

done<$LIST
