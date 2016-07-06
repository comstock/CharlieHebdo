#!/usr/bin/python

##Intended to perform a quick chick of image files in a directory structure that have specified characteristics.
##As written, this looks for the word "alpha" in the output of exiftool. I don't want alpha channels in these
##files and have tried to eliminate them. This program should help me perform a qucik check.
##
##The input text file is generated with the command, where find generates a list of all files
##in the file system using the current directory as the root, and then only passing through 
##path-and-file lines that include the word "delvierable". (I am only interested in testing
##newly created files saved in directories named "deliverable":
##
##find . -type f | grep deliverable >> [list of files.txt]


import os, sys
import re
import shutil
import subprocess
from subprocess import Popen, PIPE

imagelistDir = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/"
rootDir = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/july_drs_staging"
imagelist = imagelistDir + "images.txt"
searchstring="alpha"

f_imagelist = open(imagelist,'r')

for line in f_imagelist:
    revisedLine = re.sub("^.",rootDir, line) ; revisedLine = revisedLine.rstrip() ; # print "REV: " + revisedLine
    processLine = "exiftool " + revisedLine + " | grep " + searchstring + " --only-matching --no-messages -i" ; # print "PROC: " + processLine
##    processLine = "exiftool " + revisedLine + " | grep " + searchstring + " --only-matching --no-messages -i >> ~/exiftool_matches.txt" ; # print "PROC: " + processLine
    if os.path.isfile(revisedLine): # Does source file exist in the file system?
##        print "HERE"
        try:
            subprocess.call([processLine], shell=True)
        except IOError as detail:
            error_message = "ERROR: " + str(detail) + ":\t" + revisedLine
            e2 = error_message ; e2 = str(e2)
            print e2
    else:
        print "ELSE"
