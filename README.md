Charlie Hebdo collection processing log
================================
[comment]: # (The following is written in MarkDown and can be converted to HTML using http://daringfireball.net/projects/markdown/dingus . At least that was possible in June 2016. There also seem to be many tools for generating PDFs from MarkDown.)

To Dos
======
* Claud Maudoux has two licenses, and one file needs to be associated with one file and the other two need to be associated with the other. This is a batch deposit that will require handwork from Ming.
* Can this set of notes / instructions be copied to GitHub, where the CharlieHebdo repository is made public, and the functions are cleaned up, commented better, and renamed noting the sequence with which each is run, and where references to Harvard server names are deleted.
* Since I added the ImageMagick commands to one of the outputed files, I need to edit the convert\_to\_tiff.py script so the commands aren't duplicated or (better), I should remove the ImageMagick commands from the main script and only apply them with the _convert_ script.
* Should I leave instructions for generating text diagrams of file systems using the Tree utility?
* Nicole Mills Oral History directory includes two bitonal TIFF images -- scans of her license pages (or something like that). Should I go to the trouble of discluding bitonal TIFFs, or just delete this "oral history" directory manually, from the staging area, BEFORE RUNNING THE CONVERT TO TIFF script?

>> script that runs over targeted list of image files, and makes lists of any bitonal,  not RGB, or not 24-bit?

* Ugh. Now we have multipage TIFFs, and I have to find a way to deal with those. Need a script to identify multipage TIFFs in deliverable directories, and to break each up into a sequence of single image tiffs, and then delete the multipage tiff found in the deliverables directory.

        Convert -scene 0 abc.tif abc_%d.tif
>> [If we provide a different number, then the suffix will start with that number. For example if we mention *-scene 100* then the first image name will abc_100.tif.](http://www.techthali.org/imagemagick-splitting-multi-page-tiff-to-single-page-but-first-image-name-suffix-is-not-zero/)


* What lists do I need?

> * List of all of the files in the original file system: **masterList.txt**
* List of all of the files targeted for processing: **processingList.txt**
* List of all of the files not selected for processing: **noProcessing.txt**
* List mapping original filenames to new filenames: **filenameMapping.txt**
* Exif script file for embedding original filename within the newly named files Exif metadata: **exifOriginalFilename.txt**
* List of image processing errors and anomalies: **imageErrors.txt**
 
Step One
---------------
 Generate a list of all of the files in the collection file system. From within the root directory of the collection, execute the command:
 
        find . -type f > list\_of\_all\_files.txt

> Somewhere I need to run [a script to look for multi-page tiff images](https://github.com/comstock/CharlieHebdo/blob/master/createListmultipageTIFFS.sh), manually or by script convert them to single image scripts, replace the mulitpage images with replacement single image tiffs ** in the source directory **, regenerate a master list of files, and repeat _Step One_.

Step Two
-------------

Update the programs internal variables and run  [fileRenameMapping.py](https://github.com/comstock/fileWrangling/blob/master/fileRenameMapping.py) which generates re-organized, renamed, and reformatted copies of the collection, tuned and staged for DRS depositing. 

* Targets specific image file formats: TIFF, JPEG, PNG
* Replaces periods, spaces, hyphens in directory names with underscores
* Assumes the first level directories are named with the content donor's name
* Copies the targeted image files from the source directory to a "master" directory within the donor-named directory.
* Copies a renamed (donor-directory\_###.<ext>) image file to a "deliverable" directory within the donor-named directory (e.g., stan\_smith_001.png).
* Uses python's PIL imaging library function _Open_ to verify the image file is valid.
* Generates a list of all of the targeted image file-types identified by the script for processing.
* Generates a list of all the files in the source collection file system that were not processed and moved to the DRS staging area.
* List of all of the image files skipped over because they were identified as corrupted via PIL image.open.
* Delimited list of all of the original filenames \tab new filenames.
* Shell script that can be used to embed the original filename into the renamed image file name Exif metadata.
* Shell script that can be used to generate TIFF images from the assorted images file types found in the "deliverable" directories. ImageMagick is used to generate the TIFF files. This script is best called from [convert\_to\_tiff.py](https://github.com/comstock/CharlieHebdo/blob/master/convert_to_tiff.py) which also deletes the source image used to generate the TIFF, and it generates an error log.

Step Three
---------------
Generate the TIFF images using [convert\_to\_tiff.py](https://github.com/comstock/CharlieHebdo/blob/master/convert_to_tiff.py)

Step Four
-------------
Embed the TIFF images with the image technical metadata found in the source images by running [exiftoolValuesCopy.py](https://github.com/comstock/CharlieHebdo/blob/master/exiftoolValuesCopy.py)

Step Five
-------------
Embed newly created, new named TIFF images with the original filename:

        exiftool -overwrite_original -OriginalFileName="What's-the-fuck-par-Jo'-Graffies-2.jpg"/Jo_Graffies/deliverable/Jo_Graffies_image_001.tif

Step Six
--------

QC images:

         feh --cycle-once --no-menus --preload --recursive --slideshow-delay 3 --draw-exif --scale-down --filelist ~/DIGILAB/TEST/COMSTOCK/CharlieHebdo/LISTS/images.txt
         
         feh --list --recursive --quiet * > ../LISTS/feh_listing_qc.txt


Step Seven
-------------
* Generate a "license" directory within each donor directory.
* Copy license file from source collection file system to the appropriate license directory using [ch\_license\_copy.py](https://github.com/comstock/CharlieHebdo/blob/master/ch_license_copy.py)

Step Eight
-----------

Turn over DRS staged files to DRS depositing agent (e.g., Imaging Services).  The depositing agent will generate JPEG2000 files from the provided TIFF files, generate the DRS batch XML file, and will transfer the files in batches to DRS.
