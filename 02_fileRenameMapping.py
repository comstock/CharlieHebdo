#!/usr/bin/python
# This program was written to process of file system of digital objects regarding the Charile Hebdo murders of 7 January 2015.
# processing goals:
# From a list of all of the files in the file system, identify all image files, rename and copy them to a DRS-deposit staging area.

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

def imageValidation(sourcefile, dest, masterpath):
    logging.basicConfig(filename = img_error_log, level=logging.DEBUG, 
                    format='%(message)s:  %(name)s')
    logger=logging.getLogger(sourcefile)
    try:
        im = Image.open(sourcefile)
        print sourcefile + ": " + im.mode + ", " + im.format
        if im.mode != "RGB": # make a list of all non-RGB images, including RGB files with an extra layer (aka, RGBA), and bitonal files (aka, "1")
            error_message = sourcefile + ": " + im.mode + ", " + im.format + "\n" 
            f_img_error_log.write(error_message)
            im.convert("RGB")
    except IOError as detail:
        logger.error(detail)
        error_message = "ERROR: " + str(detail) + ":\t" + sourcefile
        e2 = error_message ; e2 = str(e2)
        f_img_error_log.write(e2)
        return e2
    else:
        try:
            shutil.copy2(sourcefile,dest) # copy the renamed image to 'deliverable' dir
        except OSError as e:
            if e.errno == 95:
                pass
        try:
            shutil.copy2(sourcefile,masterpath) # copy the source image to 'master' dir
        except OSError as e:
            if e.errno == 95:
                pass
    print "S " + sourcefile ; print "M " + masterpath
def main():
# external files and directories #
    # MS WINDOWS - un-comment #
    # 
##    dir_seperator = "\\"
##    drs_staging_path = "C:\\images\\CH\\drs\\"
##    global data_path ; data_path = "C:\\images\\CH\\data\\"
##    source_imgs_path = "C:\\images\\CH\\source\\"
    #
    # *NIX - un-comment #
    dir_seperator = "/" # *NIX
    drs_staging_path = "/media/comstock/Transcend/charliehebdo/drs_staging/"
    #drs_staging_path = "/trim/"
    global data_path ; data_path = "/media/comstock/Transcend/charliehebdo/docs/"
    source_imgs_path = "/media/comstock/Transcend/charliehebdo/original/Pictures - Charlie Archives - October 2015"
    origImg_newImg = data_path + "exifOriginalFilename.txt"
    icc_script = data_path + "icc_script.txt"
    srgb_link = data_path + "sRGB.icm"
    filenameMapping = data_path + "filenameMapping.txt"
    #
    master_list = data_path + "masterList_20160715.txt" ; print "MASTER LIST: " + master_list # The list of all files in the file system
    images_only_list = data_path + "processingList.txt" ; print "IMAGES ONLY: " + images_only_list # A list of only image files in the file system
    copy_list = data_path + "convert-to-TIFF_images_in_DRS_staging.txt" ; print "COPY LIST: " + copy_list # A *nix script for copying and renaming files
    skipped_files = data_path + "noProcessing.txt" ; print "FILES SKIPPED: " + skipped_files + "\n" # A list of non-image files not staged for DRS deposit

    # variables #
    lastOne_head = "BLAH LAST ONE HEAD"
    thisOne_head = "BLAH THIS ONE HEAD"
    firstdir = "BLAH FIRST LEVEL DIR"
    file_ext = "BLAH FILE_EXT"
    newFileName = "BLAH NEW FILE NAME"

    global img_error_log ; img_error_log = data_path + "imageErrors.txt"
    global head ; head = "BLAH HEAD"
    global tail ; tail = "BLAH TAIL"
    global error_message ; error_message = "BLAH ERROR"
    global convert_script ; convert_script = "BLAH CONVERT"
    global origNameCopy ; origNameCopy = "BLAH ORIG NAME COPY STRING"
    global origImgName ; origImgName = "BLAH ORIG NAME"
    global icc_string ; icc_string = "BLAH ICC"
    global filenameMappingText; filenameMappingText = "BLAH filenameMappingText"
    global licenseFilenameIndicator ; licenseFilenameIndicator = "Licens.*\.pdf"
    compiled_icenseFilenameIndicator = re.compile(licenseFilenameIndicator)
    
    sequence = 1
    
    image_file_types = re.compile('(jpg|jpeg|tif|tiff|png)$',re.IGNORECASE) # These are the file extentions for the image file formats targeted for deposit
    # open external files ; create external directory #
    if not os.path.exists(drs_staging_path): # this line and the following can be uncommented to create a drs staging directory in advance of copying files.
        os.makedirs(drs_staging_path)
    f_master_list = open(master_list, 'r')
    f_images_only_list = open(images_only_list, 'w')
    f_skipped_files = open(skipped_files, 'w')
    global f_img_error_log ; f_img_error_log = open(img_error_log,'w+')
    f_origImg_newImg = open(origImg_newImg,'w+')
    f_icc_script = open(icc_script,'w+')
    f_filenameMapping = open(filenameMapping, 'w')
    # from master listing of files, generate a list of only targeted image file formats #
    for line in f_master_list:
        if re.search(image_file_types,line): #Include lines ght where the file reference in the current line includes the sought after image file types.
            if not re.search(".*\/\..*", line): #Exclude lines of file references where the filename begins with a period (dotfiles)  ## TROUBLE? CHECK OU TTHIS LINE!!
                f_images_only_list.write(line)# ; f_images_only_list.write("\n")
        elif re.search(compiled_icenseFilenameIndicator,line): # don't add license files to list of skipped files (below)
            pass
        else:
            f_skipped_files.write(line)# ; f_skipped_files.write("\n")

    f_images_only_list = open(images_only_list,'r')
    f_copy_list = open(copy_list, 'w')
    for line in f_images_only_list:
        head,tail = os.path.split(line)
        tail = tail.rstrip() #; print "TAIL " + tail
        dirvalue = captureRootDir(line)
        thisOne_head = dirvalue # initialize varialbe for root dir

        if thisOne_head == lastOne_head: # if the directory cited in the current line is the same name as the previously parsed line, increment the seq number we apply to image file names.
            sequence = sequence + 1
            firstdir = dirvalue
            file_ext = re.sub(".*\.","",tail)
            file_ext = "." + file_ext ; file_ext = file_ext.rstrip()
            file_ext = file_ext.lower()
            
            copypath = drs_staging_path + firstdir + dir_seperator + "deliverable" #; print copypath
            if not os.path.exists(copypath):
                os.makedirs(copypath) 

            masterpath = drs_staging_path + firstdir + dir_seperator + "master"
            if not os.path.exists(masterpath):
                os.makedirs(masterpath)            

            newFileName = dir_seperator + firstdir + "_image_" + str("{0:03}".format(sequence)) + file_ext # assign filename
            tiffName = copypath + dir_seperator + firstdir + "_image_" + str("{0:03}".format(sequence)) + ".tif"
            #line = re.sub("^\.","",line)
            image_path = source_imgs_path + re.sub("^\.","",line)
            image_path = image_path.rstrip()# ; print "IMAGE PATH: " + image_path# ; print "DEST: " + copypath
            dest_path = copypath + newFileName ; print "COPYPATH = " + copypath + " and DEST PATH = " + dest_path
            copy_line = line.rstrip() + "\t" + copypath + newFileName + "\n" # copy command for copy_list file
##            convert_script = "convert -verbose -compress none " + copypath + newFileName + "\t-flatten -depth 8 " + tiffName + "\n" #ImageMagick file conversion command
            convert_script = copypath + newFileName + "\t" + tiffName + "\n" #Source image dir \t new image path and filename
            image_line = drs_staging_path + firstdir + newFileName ; # print image_line
            f_copy_list.write(convert_script)
            imageValidation(image_path, dest_path, masterpath) ; print "...copying " + image_path + "\n"
            origImgName = tail
##            origNameCopy = "exiftool -overwrite_original -OriginalFileName=\"" + tail + "\" " + copypath + newFileName + "\n"
            origNameCopy = "exiftool -overwrite_original -OriginalFileName=\"" + tail + "\" " + tiffName + "\n"
            f_origImg_newImg.write(origNameCopy)
            newNameStub = re.sub("\.[a-z]{3,4}$","", newFileName) ; newNameStub = re.sub(dir_seperator,"",newNameStub)#; print "STUB " + newNameStub
            icc_string = "collink -v -ip " + copypath + newFileName + " " + srgb_link + " " + data_path + newNameStub + "_TO_sRGB.icm ; cctiff -v -p -ir " + data_path + newNameStub + "_TO_sRGB.icm -e " + srgb_link + " " + copypath + newFileName + " " + copypath + dir_seperator +"sRGB_" + newNameStub + file_ext + " ; rm " + copypath + newFileName + " ; mv sRGB_" + newNameStub + file_ext + " " + newNameStub + file_ext + "\n"
            f_icc_script.write(icc_string)
            filenameMappingText = line.rstrip() + "\t" + copypath + newFileName + "\n"
            f_filenameMapping.write(filenameMappingText)
            
        else: # if root dir name for this line is different than last line processed, re-initialize seq # used in image file names.
            sequence = 1
            firstdir = dirvalue
            file_ext = re.sub(".*\.","",tail)
            file_ext = "." + file_ext ; file_ext = file_ext.rstrip()
            file_ext = file_ext.lower()
            
            copypath = drs_staging_path + firstdir + dir_seperator + "deliverable" #; print copypath
            if not os.path.exists(copypath):
                os.makedirs(copypath)             

            masterpath = drs_staging_path + firstdir + dir_seperator + "master"
            if not os.path.exists(masterpath):
                os.makedirs(masterpath)      
                
            newFileName = dir_seperator + firstdir + "_image_" + str("{0:03}".format(sequence)) + file_ext # assign filename
            tiffName = copypath + dir_seperator + firstdir + "_image_" + str("{0:03}".format(sequence)) + ".tif"
            #line = re.sub("^\.","",line)
            image_path = source_imgs_path + re.sub("^\.","",line)
            image_path = image_path.rstrip()# ; print "IMAGE PATH: " + image_path# ; print "DEST: " + copypath
            dest_path = copypath + newFileName ; print "COPYPATH = " + copypath + " and DEST PATH = " + dest_path
            copy_line = line.rstrip() + "\t" + copypath + newFileName + "\n" # copy command for copy_list file
##            convert_script = "convert -verbose -compress none " + copypath + newFileName + "\t-flatten -depth 8 " + tiffName + "\n" #ImageMagick file conversion command
            convert_script = copypath + newFileName + "\t" + tiffName + "\n" #Source image dir \t new image path and filename
            image_line = drs_staging_path + firstdir + newFileName ; # image_line for images only file
            #print copy_line
            f_copy_list.write(convert_script)            
            imageValidation(image_path, dest_path, masterpath) ; print "...copying " + image_path + "\n"
            origImgName = tail
##            origNameCopy = "exiftool -overwrite_original -OriginalFileName=\"" + tail + "\" " + copypath + newFileName + "\n"
            origNameCopy = "exiftool -overwrite_original -OriginalFileName=\"" + tail + "\" " + tiffName + "\n"
            f_origImg_newImg.write(origNameCopy)
            newNameStub = re.sub("\.[a-z]{3,4}$","", newFileName) ; newNameStub = re.sub(dir_seperator,"",newNameStub)#; print "STUB " + newNameStub
            icc_string = "collink -v -ip " + copypath + newFileName + " " + srgb_link + " " + data_path + newNameStub + "_TO_sRGB.icm ; cctiff -v -p -ir " + data_path + newNameStub + "_TO_sRGB.icm -e " + srgb_link + " " + copypath + newFileName + " " + copypath + dir_seperator +"sRGB_" + newNameStub + file_ext + " ; rm " + copypath + newFileName + " ; mv sRGB_" + newNameStub + file_ext + " " + newNameStub + file_ext + "\n"
            f_icc_script.write(icc_string)
            filenameMappingText = line.rstrip() + "\t" + copypath + newFileName + "\n"
            f_filenameMapping.write(filenameMappingText)
                        
        lastOne_head = thisOne_head # make lastOne variable equal to thisOne (directory in line just parsed)

if __name__ == "__main__":
    main()
