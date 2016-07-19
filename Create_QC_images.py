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

data_path = data_path = "/media/comstock/Transcend/charliehebdo/docs/"
source_data= data_path + "filenameMapping.txt"
source_images_path = "/media/comstock/Transcend/charliehebdo/original/Pictures - Charlie Archives - October 2015/"

##data_path = data_path = "/home/comstock/images/convert/"
##source_data= data_path + "convert_20160603.txt"


##root_dir = "/home/comstock/images/convert/"
##srgb_path = "/usr/share/color/argyll/ref/sRGB.icm"
error_log = data_path + "qc_imageFileCreation_error_log.txt"
QC_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/QC/"
##exif_target_string = "\"Profile Description\""
exifsub = "BLAH exifsub"
file_dir = "BLAH FDIR"
fileNamePrefix = "BLAH FNAME"
file_ext = "BLAH EXT"

##sed_path_parse = "(.*\/)(.*)\.([a-z]{3,4})$","\g<2>"

logging.basicConfig(filename = error_log, level=logging.DEBUG, 
                format='%(message)s:  %(name)s')

f_source_data = open(source_data,'r')

for line in f_source_data:
    line = re.sub("^\.\/","",line)
    line = source_images_path + line ; #print line
    if re.search(".*\/.*\.[a-zA-Z]{3,4}\s/",line):
        sourceFilename = re.sub("(.*\/.*\.[a-zA-Z]{3,4})\s(/.*)$","\g<1>",line); sourceFilename = sourceFilename.rstrip() #; print "SRC : " + sourceFilename
        targetFilename = re.sub("(.*\/.*\.[a-zA-Z]{3,4})\s(/.*)$","\g<2>",line); targetFilename = targetFilename.rstrip() ; print "TARGET : " + targetFilename
        targetFilenamePrefix = re.sub(".*/(.*)\.tif$","\g<1>",targetFilename); targetFilenamePrefix = targetFilenamePrefix.rstrip() ; print "PREFIX: " + targetFilenamePrefix
        QC_path_filename = QC_path + targetFilenamePrefix + ".jpg"
        processline = "convert -resize 1024 -define jpg:dct-method=fastest " + targetFilename + " " + QC_path_filename
        print processline
        try:
            subprocess.call([processline], shell=True)
        except IOError as detail:
            error_message = "ERROR: " + str(detail) + ":\t" + fileName
            e2 = error_message ; e2 = str(e2)
            print e2
    else:
        print "ELSE"
