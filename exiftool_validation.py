#!/usr/bin/python

import os, sys
import re
import shutil

imagelistDir = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/"
rootDir = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/july_drs_staging"
imagelist = imagelistDir + "images.txt"
searchstring="tiff"

f_imagelist = open(imagelist,'r')

for line in f_imagelist:
    revisedLine = re.sub("^.",rootDir, line) ; print "REV: " + revisedLine
    processLine = "exiftool " + revisedLine + " | grep " + searchstring + " --only-matching --no-messages -i" ; print "PROC: " + processLine
    
    if os.path.isfile(revisedLine): # Does source file exist in the file system?
        print "HERE"
        try:
            subprocess.call([processLine], shell=True)
        except IOError as detail:
            error_message = "ERROR: " + str(detail) + ":\t" + revisedLine
            e2 = error_message ; e2 = str(e2)
            print e2
    else:
        print "ELSE"
