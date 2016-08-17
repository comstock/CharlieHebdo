# Convert geographic data to decimal degrees format (https://en.wikipedia.org/wiki/Decimal_degrees).

import os
import re
import numpy

##inputFile="/home/comstock/DIGILAB/TEST/charliehebdo/docs/charlieHebdoLocationsMapped.csv"
##outputFile="/home/comstock/DIGILAB/TEST/charliehebdo/docs/charlieHebdoLocationsMappedOUT.csv"

inputFile="/media/comstock/Transcend/images/gps/charlieGPS.csv" # source file produced via:
                                                                # exiftool -recurse -csv -gpslatitude -gpslongitude *.tif > charlieGPS.csv
                                                                
outputFile="/media/comstock/Transcend/images/gps/charlieGPS_OUT.csv"

lineNumber = 1
countArray=[]
Lat = "" ; Lon = "" ; FileName = ""

f_inputFile = open(inputFile, 'r')
f_outputFile = open (outputFile, 'w')

fileName = re.compile("(^.*)(,\"\d.*$)")
degMatch = re.compile("\"((\d){1,2}) deg .*",re.DOTALL)
minMatch = re.compile(".* ((\d|\.){1,9})\'.*",re.DOTALL)
secMatch = re.compile(".* ((\d|\.){1,9})\".*",re.DOTALL)

for line in f_inputFile:
    count = line.count(",") ; #print "line "on + str(lineNumber) + " : commas = " + str(count)
    if lineNumber == 1:
        cummulativeCount = count
    else:
        cummulativeCount = cummulativeCount + count
    countArray.append(count)
    lineNumber = lineNumber + 1

    if re.search(degMatch, line):
        columns = line.split(",")
        for column in columns:
            if re.search("N", column):
                Lat = column; print "Lat: " + Lat
                LatDegree = re.sub(degMatch,"\g<1>",Lat) ; print "LatDegree: " + LatDegree
                LatMinutes = re.sub(minMatch,"\g<1>", Lat) ; print "LatMinutes = " + str(LatMinutes)
                LatSeconds = re.sub(secMatch,"\g<1>", Lat) ; print "LatSeconds = " + str(LatSeconds)
                LatLocation = float(LatDegree) + (float(LatMinutes)/60) + (float(LatSeconds)/3600) ;  print "Latloc : " + str(LatLocation)
            elif re.search("S", column):
                Lat = column; print "Lat: " + Lat
                LatDegree = re.sub(degMatch,"\g<1>",Lat) ; print "LatDegree: " + LatDegree
                LatMinutes = re.sub(minMatch,"\g<1>", Lat) ; print "LatMinutes = " + str(LatMinutes)
                LatSeconds = re.sub(secMatch,"\g<1>", Lat) ; print "LatSeconds = " + str(LatSeconds)
                LatLocation = float(LatDegree) - (float(LatMinutes)/60) - (float(LatSeconds)/3600) ;  print "Latloc : " + str(LatLocation)
            elif re.search("E",column):
                Lon = column; print "Lat: " + Lat
                LonDegree = re.sub(degMatch,"\g<1>",Lon) ; print "LonDegree: " + LonDegree
                LonMinutes = re.sub(minMatch,"\g<1>", Lon) ; print "LonMinutes = " + str(LonMinutes)
                LonSeconds = re.sub(secMatch,"\g<1>", Lon) ; print "LonSeconds = " + str(LonSeconds)
                LonLocation = float(LonDegree) + (float(LonMinutes)/60) + (float(LonSeconds)/3600) ;  print "Lonloc : " + str(LonLocation)
            elif re.search("W",column):
                Lon = column; print "Lat: " + Lat
                LonDegree = re.sub(degMatch,"\g<1>",Lon) ; print "LonDegree: " + LonDegree
                LonMinutes = re.sub(minMatch,"\g<1>", Lon) ; print "LonMinutes = " + str(LonMinutes)
                LonSeconds = re.sub(secMatch,"\g<1>", Lon) ; print "LonSeconds = " + str(LonSeconds)
                LonLocation = float(LonDegree) - (float(LonMinutes)/60) - (float(LonSeconds)/3600) ;  print "Lonloc : " + str(LonLocation)
            else:
                FileName = column        
        outputLine = FileName + "\t" + str(LatLocation) + "," + str(LonLocation) + "\n" ; print outputLine 
        print LatDegree
        print LatMinutes
        print LatSeconds
        
        f_outputFile.write(outputLine)
    else: pass

countMean = numpy.mean(countArray) ; countMean = int(numpy.ceil(countMean)) ; print countMean #get integer mean number of commas per line
##print countArray
columnCount = countMean + 1
