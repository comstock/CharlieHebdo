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

data_path = data_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/comstock_notes/scripts/scripted_reports/"
source_data= data_path + "filenameMapping_TIFF.txt"
source_images_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/CH_round_3/Pictures - Charlie Archives - October 2015/"

##data_path = data_path = "/home/comstock/images/convert/"
##source_data= data_path + "convert_20160603.txt"


##root_dir = "/home/comstock/images/convert/"
##srgb_path = "/usr/share/color/argyll/ref/sRGB.icm"
error_log = data_path + "convert_to_tiff_error_log.txt"
##exif_target_string = "\"Profile Description\""
exifsub = "BLAH exifsub"
file_dir = "BLAH FDIR"
fileNamePrefix = "BLAH FNAME"
file_ext = "BLAH EXT"
sed_path_parse = "(.*\/)(.*)\.([a-z]{3,4})$","\g<2>"

logging.basicConfig(filename = error_log, level=logging.DEBUG, 
                format='%(message)s:  %(name)s')

f_source_data = open(source_data,'r')

for line in f_source_data:
    line = re.sub("^\.\/","",line)
    line = source_images_path + line ; #print line
    if re.search(".*\/.*\.[a-zA-Z]{3,4}\s/",line):
        sourceFilename = re.sub("(.*\/.*\.[a-zA-Z]{3,4})\s/.*$","\g<1>",line); print "SRC : " + sourceFilename
    
##    exiftool WID-AFR.jpg -tagsfromfile @ -srcfile WID-AFR.tif -XMP:format=TIFF
    
    
##    fileNamePrefix = re.sub("(.*\/)(.*)\.([a-z]{3,4})$","\g<2>",line) ; print "FILENAME PREFIX = :" + fileNamePrefix
####    file_dir = source_images_path + line
##    file_dir = re.sub("(.*\/)(.*)\.([a-z]{3,4})\t.*$","\g<1>",line) ; print "DIR NAME = :" + file_dir
##    file_ext = re.sub("(.*\/)(.*)\.([a-z]{3,4})\t.*","\g<3>",line) ; print "FILE EXT = :" + file_ext
##    fileName = file_dir.rstrip() + fileNamePrefix.rstrip() + "." + file_ext.rstrip() ; print fileName
##    if os.path.isfile(fileName):
##        processline = "convert -verbose -compress none " + line ; print "PROC " + processline
##        try:
##            subprocess.call([processline], shell=True)
##            os.remove(fileName)
##        except IOError as detail:
##            error_message = "ERROR: " + str(detail) + ":\t" + fileName
##            e2 = error_message ; e2 = str(e2)
##            print e2
##    else:
##        print "ELSE"
##
##
##def imageValidation(sourcefile, dest, masterpath):
##    logging.basicConfig(filename = img_error_log, level=logging.DEBUG, 
##                    format='%(message)s:  %(name)s')
##    logger=logging.getLogger(sourcefile)
##    try:
##        im = Image.open(sourcefile)
##    except IOError as detail:
##        logger.error(detail)
##        error_message = "ERROR: " + str(detail) + ":\t" + sourcefile
##        e2 = error_message ; e2 = str(e2)
##        return e2


