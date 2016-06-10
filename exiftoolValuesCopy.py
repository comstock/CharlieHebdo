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
        sourceFilename = re.sub("(.*\/.*\.[a-zA-Z]{3,4})\s(/.*)$","\g<1>",line); sourceFilename = sourceFilename.rstrip() ; print "SRC : " + sourceFilename
        targetFilename = re.sub("(.*\/.*\.[a-zA-Z]{3,4})\s(/.*)$","\g<2>",line); targetFilename = targetFilename.rstrip() ; print "TARGET : " + targetFilename
        processline = "exiftool -tagsfromfile \"" + sourceFilename + "\" " + targetFilename + " -XMP:format=" ; print "PROC " + processline
        try:
            subprocess.call([processline], shell=True)
        except IOError as detail:
            error_message = "ERROR: " + str(detail) + ":\t" + fileName
            e2 = error_message ; e2 = str(e2)
            print e2
    else:
        print "ELSE"
