#!/usr/bin/python
#
# Take filenameMapping (original filename <tab>  newfilename) text file, strip our directory paths and generate a CSV file that can be impoted into a spreadsheet.
#
import os
import subprocess
from subprocess import Popen, PIPE
import PIL
from PIL import ImageCms
import re
import logging

fileList = "/home/comstock/Desktop/filenameMapping.txt"
twoColumnMappingFile = "/home/comstock/Desktop/twoColumnMappingFile.csv"
f_fileList = open(fileList, 'r')
f_twoColumnMappingFile = open(twoColumnMappingFile, 'w')

image_file_types = re.compile('(jpg|jpeg|tif|tiff|png)$',re.IGNORECASE) # These are the file extentions for the image file formats targeted for deposit

for line in f_fileList:
    if re.search(image_file_types,line):
        head, tail = os.path.split(line)
        left = head ; right = tail
##        left = re.sub("^\.\/.*\/(.*\.[a-z]{3,4})$","\g<1>",left) 
        left = re.sub("\t\/.*deliverable.*","",left); ignore,left = os.path.split(left)
        right = tail
        print "HEAD:" + head ; print "TAIL: " + tail
        row = left + "\t" + right
        f_twoColumnMappingFile.write(row)
