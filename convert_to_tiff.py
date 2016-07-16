#!/usr/bin/python
# Runs argyll utiles to generate appropriately ICC profiled images.
#
import os
import subprocess
from subprocess import Popen, PIPE
import PIL
from PIL import ImageCms
import re
import logging

global targetFileName ; targetFileName = "BLAH_targetFileName"

##def imageValidation(targetFileName):
##    logging.basicConfig(targetFileName = img_error_log, level=logging.DEBUG, 
##                    format='%(message)s:  %(name)s')
##    logger=logging.getLogger(targetFileName)
##    try:
##        im = Image.open(targetFileName)
##    except IOError as detail:
##        logger.error(detail)
##        error_message = "VALIDATION ERROR: " + str(detail) + ":\t" + targetFileName
##        e2 = error_message ; e2 = str(e2)
##        print e2 ; #return e2

def main():
    data_path = data_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/comstock_notes/finalAttempt/"
    source_data= data_path + "convert-to-TIFF_images_in_DRS_staging.txt"

    ##data_path = data_path = "/home/comstock/images/convert/"
    ##source_data= data_path + "convert_20160603.txt"



    ##root_dir = "/home/comstock/images/convert/"
    ##srgb_path = "/usr/share/color/argyll/ref/sRGB.icm"
    error_log = data_path + "convert_to_tiff_error_log.txt"
    f_error_log = open(error_log, 'w')
    ##exif_target_string = "\"Profile Description\""
##    exifsub = "BLAH exifsub"
##    file_dir = "BLAH FDIR"
##    fileNamePrefix = "BLAH FNAME"
##    file_ext = "BLAH EXT"
##    sed_path_parse = "(.*\/)(.*)\.([a-z]{3,4})$","\g<2>"

    logging.basicConfig(filename = error_log, level=logging.DEBUG, 
                    format='%(message)s:  %(name)s')

    f_source_data = open(source_data,'r')

    for line in f_source_data:
        sourceFileName = re.sub("^(.*)(\t.*)","\g<1>", line) ; sourceFileName = sourceFileName.rstrip() ; print "sourceFileName: " + sourceFileName
        targetFileName = re.sub("^(.*)(\t.*)","\g<2>", line) ; targetFileName = targetFileName.rstrip() ; print "targetFileName: " + targetFileName
    ##    fileNamePrefix = re.sub("(.*\/)(.*)\.([a-z]{3,4})$","\g<2>",line) ; print "FILENAME PREFIX = :" + fileNamePrefix
    ##    file_dir = re.sub("(.*\/)(.*)\.([a-z]{3,4})\t.*$","\g<1>",line) ; print "DIR NAME = :" + file_dir
    ##    file_ext = re.sub("(.*\/)(.*)\.([a-z]{3,4})\t.*","\g<3>",line) ; print "FILE EXT = :" + file_ext
    ##    fileName = file_dir.rstrip() + fileNamePrefix.rstrip() + "." + file_ext.rstrip() ; print fileName
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
