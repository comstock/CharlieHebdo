#!/usr/bin/python
# Runs argyll utiles to generate appropriately ICC profiled images.
#
import os
import subprocess
from subprocess import Popen, PIPE
##os.spawn*
##os.popen*
##popen2.*
##commands.*
import re

root_dir = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/DAVID_XCHANGE"
srgb_path = "/usr/share/color/argyll/ref/sRGB.icm"
exif_target_string = "Profile Description"
exifsub = "BLAH exifsub"


find_file_str = "find " + root_dir + "/ -name *.tif > /home/comstock/images/icc_tiffs.txt"
print find_file_str
subprocess.call(find_file_str, shell=True)
fl = open("/home/comstock/images/icc_tiffs.txt",'r')

for line in fl:
    fname = re.sub("^.*\/(.*)\.[a-z]{3,4}","\g<1>", line) ; print "FileName " + fname
    dirpath = re.sub("(^.*)\/\w+\.[a-z]{3,4}","\g<1>", line) ; print "DirPath " + dirpath
    exifsub = "exiftool -v " + line + " | grep \"" + exif_target_string + "\""
    try:
        exifdata = subprocess.call([exifsub], shell=True) ; print exifdata
        if re.search(exif_target_string,exifdata):
            icc_conversion = "collink -v -ir " + line + " " + srgb_path + " " + "srgb_" + f_prefix + ".icm ; cctiff -v -p -ir " + line + " " + "-e srgb_" + f_prexix + ".icm " + line + " " + path + "srgb_" + f_prefix + ".tif"
            print "ICC CONVERSION: " + icc_conversion
            print "ICC APPLICATION: " + icc_application
        else:
            icc_application = "cctiff -P -v -e " + srgb_path + " " + line + " " + dirpath + fname + "\n"
            print "NO PROF " + line
    except:
        print "Error"
        pass


##subprocess.call(["cd /home/comstock/images/CH/drs/"], shell=True)
##
####os.chdir(/home/comstock/images/CH/drs)
##fl = "/home/comstock/images/CH/icc_filelist.txt"
##f = open(fl,'w')
##f.write = subprocess.call(find_file_str, shell=True)
    
    

##temp = subprocess.call(find_file_str, shell=True) ; print temp
#f.write(temp)


##for line in f:
##    dir = re.sub("\.[a-Z](3,4)","",line)
##    subprocess.call(["cd dir"])
##    subprocess.call(["find . -type f | convert line -profile icc_filename -profile sRGB line"], shell=True)
    
##
####find . -type f > filelist.txt
##while read line
##do exiftool -icc_profile -b -w icc $line
##done < filelist.txt
##
##while read line
##do
##icc_filename = sed 's/\.*$/icc/'
##icc_filename = sed 's/icc/\.icc/'
##echo icc_filename
##convert $line -profile icc_filename -profile sRGB.icc $line
##
###
###
##echo "
##     ~~~~~ FIN ~~~~~
##"
####cd /cygdrive/c/images/CH/drs/
####pwd
####find . -type d | while read line ;
####do DIR = sed 's/\/\w*\.([a-z](3,4))//' ;
####echo "DIR "DIR ;
####cd DIR ;
####find . -type f | while read line ; do convert $line -profile icc_filename -profile sRGB.icc $line ; done
####done
