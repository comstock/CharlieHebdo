import os, sys
import re
import shutil
#import PIL
from PIL import Image
import logging

def captureRootDir(line):
        dir = os.path.dirname(line)
        dir = re.sub("^\.\/","",dir)    # remove ./ from line beginning
        dir = re.sub("[\s\.,\'\`]","_",dir)      # substitute blank spaces, periods, commas, and asterisks with underscores
        dir = re.sub("\/.*","",dir)     # Only capture the first directory name. After the /, delete all.
        return(dir)

def main():

    # Variables #
    dir_seperator = "/" # *NIX
    drs_staging_path = "/media/comstock/Transcend/charliehebdo/drs_staging/"
    global data_path ; data_path = "/media/comstock/Transcend/charliehebdo/docs/"
    source_imgs_path = "/media/comstock/Transcend/charliehebdo/original/Pictures - Charlie Archives - October 2015/"
    origImg_newImg = data_path + "exifOriginalFilename.txt"
    filenameMapping = data_path + "filenameMapping.txt"
    #
    master_list = data_path + "masterList_20160715.txt" ; print "MASTER LIST: " + master_list # The list of all files in the file system
##    licenseList = data_path + "licenseList.txt"
    licenseList = master_list
    licenseDir = "license"
    global licenseFilenameIndicator ; licenseFilenameIndicator = "Licens.*\.pdf"
    compiled_icenseFilenameIndicator = re.compile(licenseFilenameIndicator)
    
    
    global img_error_log ; img_error_log = data_path + "imageErrors.txt"
    global head ; head = "BLAH HEAD"
    global tail ; tail = "BLAH TAIL"
    global error_message ; error_message = "BLAH ERROR"
    global convert_script ; convert_script = "BLAH CONVERT"
    global origNameCopy ; origNameCopy = "BLAH ORIG NAME COPY STRING"
    global origImgName ; origImgName = "BLAH ORIG NAME"
    global filenameMappingText; filenameMappingText = "BLAH filenameMappingText"

    f_licenseList = open(licenseList,'r')

    for line in f_licenseList:
        if re.search(compiled_icenseFilenameIndicator,line):
            dirvalue = captureRootDir(line)
            head,tail = os.path.split(line)
            tail = tail.rstrip()
            licenseSource = re.sub("^.","",line) ; licenseSource = licenseSource.rstrip()
            licenseSource = source_imgs_path + line.rstrip()
            licensePath = drs_staging_path + dirvalue + dir_seperator + licenseDir
            licenseDest = drs_staging_path + dirvalue + dir_seperator + licenseDir + dir_seperator + tail ; print "LICENSE DEST: " + licenseDest
            if not os.path.exists(licensePath):
                os.makedirs(licensePath)
            try:
                shutil.copy2(licenseSource,licenseDest) # copy license to "license" dir
            except OSError as e:
                if e.errno == 95:
                    pass        
        
if __name__ == "__main__":
    main()
