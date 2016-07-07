#!/bin/bash
# List of donor supplied tiffs generated with the following command:
#
# find . -type f | grep -G -i '.*master.*\.tif' > ../LISTS/masterTiffs.txt
#
masterTiffs="/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/masterTiffs.txt"

while read line; do
exiftool "$line" | grep -i multi-page; echo "multipage TIFF: $line" >> tiffID_log.txt
# identify -verbose -format "%p " "$line" >> tiffID_log.txt
done < $masterTiffs
