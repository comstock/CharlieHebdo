#!/usr/bin/python

import os,sys

dataDirectory = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/LISTS/"
dataFile = dataDirectory + "listoftiffs.txt"
filesNotFound = dataDirectory + "filesNotFound.txt"

f_filesNotFound = open(filesNotFound,'w')

#Your path here e.g. "C:\Program Files\text.txt"
#if os.path.exists("C:\..."):

if os.path.isfile(dataFile):
  print "FOUND: " + dataFile
else:
  print "MISSING: " + dataFile
  f_filesNotFound.write(dataFile)
