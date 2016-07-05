#!/bin/bash
# run exiftool on a dynamically generated list of image files, and 
# list the filenames when the searched for metadata string is found.

DIR="/home/comstock/images/"
LIST=$DIR"images.txt"
SEARCHSTRING="Alpha"

find $DIR -name *.tif > $LIST

while read LINE
do
    exiftool $LINE | grep $SEARCHSTRING -l
done < $LIST
