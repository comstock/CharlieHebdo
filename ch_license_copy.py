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
    dir_list = "test_files_list.txt"

    drs_staging_path = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/drs_staging/"
    data_source = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/comstock_notes/scripts/scripted_reports/"
    consent_docs_root = "/run/user/1000/gvfs/smb-share:server=pentos-smb.ad.hcl.harvard.edu,share=digilab/TEST/COMSTOCK/CharlieHebdo/CH_round_3/Pictures - Charlie Archives - October 2015/"
    error_log = data_source + "consent_copy_error_log.txt"
    dirlist_path = data_source + dir_list #; print dirlist_path

    f_dirlist_path = open(dirlist_path,'r')
    f_error_log = open(error_log,'w')
    
    lastOne = "BLAH LAST ONE"
    thisOne = "BLAH THIS ONE"
    
    for line in f_dirlist_path:
        origdir = os.path.dirname(line) #; print "ORIGDIR: " + origdir
        thisOne = origdir
        
        if lastOne != thisOne and re.search("onsent.*(pdf|doc|PDF|DOC|docx|DOC)",line):

                trimline = line.rstrip() ; trimline = re.sub("^\.\/","",trimline) ; trimline = consent_docs_root + trimline
                origname = re.sub(".*(\/.*\.[a-zA-Z]{3,4})$","\g<1>",line) ; print "ORIG NAME: " + origname
                newdirvalue = captureRootDir(line)
                newdirvalue = newdirvalue +"/"
                dest =  drs_staging_path + "license/" + newdirvalue
                if not os.path.exists(dest):
                    os.makedirs(dest)            
                print trimline + "\t" + dest + "\n"
##                try:
##                    shutil.copy2(trimline,newdirvalue)
##                except:
##                    error = "ERROR copying" + timeline + "\t" + newdirvalue
##                    f_error_log.write(error)
        lastOne = thisOne
                
    
if __name__ == "__main__":
    main()
