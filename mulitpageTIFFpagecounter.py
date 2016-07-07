import re
from PIL import Image

masterTiffs = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/masterTiffs.txt"
dataroot = "/home/comstock/DIGILAB/TEST/COMSTOCK/CharlieHebdo/july_drs_staging"
##dataroot = "/home/comstock/images"
##masterTiffs = "/home/comstock/images/masterTiffs.txt"

f_masterTiffs = open(masterTiffs,'r')

for line in f_masterTiffs:
    n = 0 # a single image tiff will only have an image at index 0
    filepath = re.sub("^.","",line) ; filepath = dataroot + filepath ; filepath = filepath.rstrip() ; print filepath
    im = Image.open(filepath)
    while True:
        try:
            im.seek(n)
            n = n + 1
        except EOFError:
            print "GOT EOF Error when I tried to load " + str(n) # n = the total number of images in the TIFF. More than 1 = multipage.
            break;
