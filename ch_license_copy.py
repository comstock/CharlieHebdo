import os
import sys
import shutil

import re

def captureRootDir(linefromfile):
        dir = os.path.dirname(linefromfile)
        dir = re.sub("^\.\/","",dir)    # remove ./ from line beginning
        dir = re.sub("\s","_",dir)      # substitute blank spaces with underscores
        dir = re.sub("\/.*","",dir)     # Only capture the first directory name. After the /, delete all.
        return(dir)

def main():
##    dir_list = "ch_orig_pict_dir_list.txt"
##    dir_list = "test_files_list.txt"
    dir_list = "fileList_20160519.txt"

    drs_staging_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/drs_staging/"
    data_source = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/comstock_notes/scripts/scripted_reports/"
    consent_docs_root = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/CH_round_3/Pictures - Charlie Archives - October 2015/"
    error_log = data_source + "consent_copy_error_log.txt"
    dirlist_path = data_source + dir_list #; print dirlist_path
    copyscript = data_source + "licenseCopyScript.txt"

    f_dirlist_path = open(dirlist_path,'r')
    f_error_log = open(error_log,'w')
    f_copyscript = open(copyscript,'w')
    
    lastOne = "BLAH LAST ONE"
    thisOne = "BLAH THIS ONE"
    
    for line in f_dirlist_path:
        origdir = os.path.dirname(line) #; print "ORIGDIR: " + origdir
        thisOne = origdir
        
        if lastOne != thisOne and re.search("onsent.*(pdf)",line,re.IGNORECASE):

                trimline = line.rstrip() ; trimline = re.sub("^\.\/","",trimline) ; trimline = consent_docs_root + trimline
                origname = re.sub(".*(\/.*\.[a-zA-Z]{3,4})$","\g<1>",line) ; print "ORIG NAME: " + origname
                origname = origname.rstrip()
                newdirvalue = captureRootDir(line)
                newdirvalue = newdirvalue +"/"
                dest =  drs_staging_path + newdirvalue + "license"
                copypath = dest + origname
                if not os.path.exists(dest):
                    os.makedirs(dest)            
                print trimline + "\t" + dest + "\n"
                copyscriptText = "cp " + trimline + "\t" + dest + "\n"
                f_copyscript.write(copyscriptText)              
                try:
                    shutil.copy2(trimline,copypath)
                except OSError as detail:
                    if detail.errno == 95:
                        pass
                    error_message = "ERROR: "+ str(detail) + ": " + trimline
                    f_error_log.write(error_message)
        elif lastOne != thisOne and re.search("onsent.*(doc|docx)",line,re.IGNORECASE):

                trimline = line.rstrip() ; trimline = re.sub("^\.\/","",trimline) ; trimline = consent_docs_root + trimline
                origname = re.sub(".*(\/.*\.[a-zA-Z]{3,4})$","\g<1>",line) ; print "ORIG NAME: " + origname
                origname = origname.rstrip()
                newdirvalue = captureRootDir(line)
                newdirvalue = newdirvalue +"/"
                dest =  drs_staging_path + newdirvalue + "license"
                copypath = dest + origname
                if not os.path.exists(dest):
                    os.makedirs(dest)            
                print trimline + "\t" + copypath + "\n"
                copyscriptText = "cp " + trimline + "\t" + copypath + "\n"
                f_copyscript.write(copyscriptText)
                try:
                    shutil.copy2(trimline,copypath)
                except OSError as detail:
                    if detail.errno == 95:
                        pass
                    error_message = "ERROR: "+ str(detail) + ": " + trimline
                    f_error_log.write(error_message)
        lastOne = thisOne
                
    
if __name__ == "__main__":
    main()
