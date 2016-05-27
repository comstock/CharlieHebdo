#!/bin/bash
# Runs Exiftool to generate a listing of icc profiles from source images
#
while read line
do exiftool -icc_profile -b -w icc $line > ../data/icc_profile_list.txt
done < ../data/imageFilesOnly.txt
#
#
echo "
     ~~~~~ FIN ~~~~~
"
# exiftool -icc_profile -b -w icc image.jpg
