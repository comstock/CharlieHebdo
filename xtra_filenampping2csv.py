#!/usr/bin/python
#
# takes a text file where each line is path + original filename \tab path + copy of original file, renamed
# and generates a two column filename mapping file where the left column is the orig filemane and reight column is renamed version of same image file.
# The file only parses lines that references specific image file types as specified by their file extensions, and ignores lines that do not meet the 
# image file extension search criteria.
#
# Note: to take the renamed file extension and change it to 'jp2', to reflect the file format of the file deposited to DRS, you can use the following
# command:
#
# cat ~/[path]/filenameMapping.txt | sed 's/[a-z]\{3,4\}$/jp2/'
#
import os
import re

fileList = "/home/comstock/Desktop/filenameMapping_jp2.txt"
twoColumnMappingFile = "/home/comstock/Desktop/twoColumnMappingFile.csv"
f_fileList = open(fileList, 'r')
f_twoColumnMappingFile = open(twoColumnMappingFile, 'w')

image_file_types = re.compile('(jpg|jpeg|tif|tiff|png)(\s|$)',re.IGNORECASE) # These are the file extentions for the image file formats targeted for deposit.

for line in f_fileList:
    if re.search(image_file_types,line): # if line has targeted image file extension...
        head, tail = os.path.split(line) # split original filename and renamed filename into variables 'head' and 'tail'.
        left = head ; right = tail
        left = re.sub("\t\/.*deliverable.*","",left) #left = path plus orignal filename with tab and following path-to-renamed file deleted.
        ignore,left = os.path.split(left) #Split path from original filename where path = 'ignore" var and left = orignal filename.
##        print "HEAD:" + head ; print "TAIL: " + tail
        print "ORIGINAL FNAME:\t" + left ; print "RE-WRITTEN FNAME:\t" + right
        row = left + "\t" + right # define encoding for each row of two column, tab delimited, mapping file.
        f_twoColumnMappingFile.write(row) #write out file
