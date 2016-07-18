#!/usr/bin/python
#
import os
import subprocess
from subprocess import Popen, PIPE
import PIL
from PIL import ImageCms
import re
import logging

global targetFileName ; targetFileName = "BLAH_targetFileName"

def main():
    data_path = data_path = "/media/comstock/Transcend/charliehebdo/docs/"
    source_data= data_path + "convert-to-TIFF_images_in_DRS_staging.txt"
    error_log = data_path + "convert_to_tiff_error_log.txt"
    f_error_log = open(error_log, 'w')

    logging.basicConfig(filename = error_log, level=logging.DEBUG, 
                    format='%(message)s:  %(name)s')

    f_source_data = open(source_data,'r')

    for line in f_source_data:
        sourceFileName = re.sub("^(.*)(\t.*)","\g<1>", line) ; sourceFileName = sourceFileName.rstrip() ; print "sourceFileName: " + sourceFileName
        targetFileName = re.sub("^(.*)(\t.*)","\g<2>", line) ; targetFileName = targetFileName.rstrip() ; print "targetFileName: " + targetFileName
        if os.path.isfile(sourceFileName): # Does source file exist in the file system?
            print "HERE"
##            processline = "convert -verbose -compress none " + sourceFileName + " -flatten -depth 8 " + targetFileName ; print "PROC " + processline
            processline = "convert -verbose -compress none " + sourceFileName + " -alpha remove -alpha off -flatten -depth 8 " + targetFileName ; print "PROC " + processline
##            processline = "mogrify -verbose -depth 8 -set colorspace rgb -compress none  -format tif -alpha remove " + sourceFileName
    ##        processline = line ; print "PROC " + processline
            try:
                subprocess.call([processline], shell=True)
                if not os.path.isfile(targetFileName): # TROUBLE? LOOK HERE!!!!!!!!!!!
                    os.remove(sourceFileName)
                else:
                    tiffCreateError = targetFileName + " NOT CREATED! [convert_to_tiff.py] \n"
                    f_error_log.write(tiffCreateError)
            except IOError as detail:
                error_message = "ERROR: " + str(detail) + ":\t" + sourceFileName
                e2 = error_message ; e2 = str(e2)
                print e2
        else:
            print "ELSE"
            
if __name__ == "__main__":
    main()
