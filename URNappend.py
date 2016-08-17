# Adds image URN to table of filenames, GPSlocations to make the output suitable for Google-mapping using Google Fusion Tables.

import os
import re

URNFile="/media/comstock/Transcend/images/gps/gps_urn.txt"  # generated from DRS deposit file via: 
                                                            # awk '/JP2/ {print "http://nrs.harvard.edu/"$11"\t"$5}' Fabien_B6167982090676897383.txt > gps_urn.txt
                                                            
CSVFile="/media/comstock/Transcend/images/gps/charlieGPS_OUT.csv"   # generated via:
                                                                    # exiftool -recurse -csv -gpslatitude -gpslongitude *.tif > charlieGPS.csv
                                                                    # subsequently processed via decimalDegrees.py into charlieGPS_OUT.csv
                                                                    
OUT_CSVFile = "/media/comstock/Transcend/images/gps/charlieGPS_OUT_wURN.csv" # Output file from this script.

##f_URNFile = open(URNFile,'r')
f_CSVFile = open(CSVFile,'r')
f_OUT_CSVFile = open(OUT_CSVFile,'w')
outputLine = "img filename\tlocation\tURN\n" ; f_OUT_CSVFile.write(outputLine)

for CSVline in f_CSVFile:
    print "CSVline: " + CSVline
    LOC = re.sub("^.*\t(.*)","\g<1>",CSVline) ; LOC = LOC.rstrip() ; print "loc: " + LOC
    f_URNFile = open(URNFile,'r') # instead of opening and closing the URNFile, maybe I could load the values of the file into an array for speedier processing.
    for URNLine in f_URNFile:
        OSN = re.sub("(^.*)\t(.*$)","\g<2>",URNLine) ; OSN = OSN.rstrip() ; print "osn: " + OSN
        URN = re.sub("(^.*)\t(.*$)","\g<1>",URNLine) ; URN = URN.rstrip() ; print "urn: " + URN
        if re.search(OSN,CSVline):
            CSVrow = CSVline.rstrip()
            outputLine = OSN + "\t" + LOC + "\t" + URN + "\n"; print "out: " + outputLine
            f_OUT_CSVFile.write(outputLine)
    f_URNFile.close()
