#!/bin/bash
# List of donor supplied tiffs generated with the following command:
#
# find . -type f | grep -G -i '.*master.*\.tif' > ../LISTS/masterTiffs.txt
#
masterTiffs="/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/masterTiffs.txt"

while read line; do
# doesn't work. You cannot count on a tiff having the word "multi-page" in the SubFile Type tag to indicate multipage tiff.
# I downloaded an example multipage TIFF and it had no SubFile Type value.
exiftool "$line" | grep -i multi-page; echo "multipage TIFF: $line" >> tiffID_log.txt
# identify -verbose -format "%p " "$line" >> tiffID_log.txt
done < $masterTiffs
