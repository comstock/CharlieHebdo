#!/bin/bash
# run exiftool on a dynamically generated list of image files, and 
# list the filenames when the searched for metadata string is found.

DIR="/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/"
LIST=$DIR"images.txt"
SEARCHSTRING="tiff"

## TO DO: The images.txt file only gives a relative path to the file. Fix that and the script should find the files.

# find $DIR -name *.tif > $LIST

while read LINE
do
	exiftool "$LINE" | grep $SEARCHSTRING --only-matching --no-messages -i
	#echo $LINE
done < $LIST
