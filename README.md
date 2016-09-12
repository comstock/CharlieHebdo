Charlie Hebdo collection processing log
================================
[comment]: # (The following is written in MarkDown and can be converted to HTML using http://daringfireball.net/projects/markdown/dingus . At least that was possible in June 2016. There also seem to be many tools for generating PDFs from MarkDown.)

To Dos
======
* Claud Maudoux has two licenses, and one file needs to be associated with one file and the other two need to be associated with the other. This is a batch deposit that will require handwork from Ming.

> * Claude_Maudoux_License_1.pdf is a license for photographs: Claude_Maudoux_image_001.tif and Claude_Maudoux_image_001.tif

> * Claude_Maudoux_License_2.pdf is a license for drawing: Claude_Maudoux_image_003.tif

* If atypical TIFF files fail conversion to JP2 (see: ./docs/files\_with\_alpha\_channels.txt), these files will have to be specially processed.

* What lists do we need?

> * List of all of the files in the original file system: **masterList.txt**
* List of all of the files targeted for processing: **processingList.txt**
* List of all of the files not selected for processing: **noProcessing.txt**
* List mapping original filenames to new filenames: **filenameMapping.txt**
* Exif script file for embedding original filename within the newly named files Exif metadata: **exifOriginalFilename.txt**
* List of image processing errors and anomalies: **imageErrors.txt**

## Processing sequence
------------------------------------

1.
-----
 Generate a list of all of the files in the collection file system. From within the root directory of the collection, execute the command:

        find . -type f > list_of_all_files.txt

2.
------

Update the programs internal variables and run  [fileRenameMapping.py](https://github.com/comstock/CharlieHebdo/blob/master/02_fileRenameMapping.py) which generates re-organized, renamed, and reformatted copies of the collection, tuned and staged for DRS depositing.

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
* [convert\_to\_tiff.py](https://github.com/comstock/CharlieHebdo/blob/master/04_convert_to_tiff.py) converts non-TIFF images to TIFF format, and also deletes the source image used to generate "deliverable" image.

3.
-----
[Copy licenses](https://github.com/comstock/CharlieHebdo/blob/master/03_ch_license_copy.py) (all in PDF format) to "license" directory in DRS staging area


4.
-----
Generate the TIFF images using [convert\_to\_tiff.py](https://github.com/comstock/CharlieHebdo/blob/master/04_convert_to_tiff.py)

5.
-----
Embed the TIFF images with the image technical metadata found in the source images by running [exiftoolValuesCopy.py](https://github.com/comstock/CharlieHebdo/blob/master/05_exiftoolValuesCopy.py)

6.
-----
Embed newly created, new named TIFF images with the original filename:

        exiftool -overwrite_original -OriginalFileName="What's-the-fuck-par-Jo'-Graffies-2.jpg" /Jo_Graffies/deliverable/Jo_Graffies_image_001.tif

Quality control
-----

7.a
-----

The following generates a text table of files found in the "deliverable" directories, including notations of images with ALPHA channels


         feh --list --recursive --quiet * | grep deliverable > ../docs/feh_listing_qc.txt

7.b
-----

Run [xtra_filenampping2csv.py](https://github.com/comstock/CharlieHebdo/blob/master/xtra_filenampping2csv.py) to generate a delimited text file that maps the originally provided filename to the name of the file deposited to DRS.

DRS deposit
-----

8.
-----

Turn over DRS staged files to DRS depositing agent (e.g., Imaging Services).  The depositing agent will generate JPEG2000 files from the provided TIFF files, generate the DRS batch XML file, and will transfer the files in batches to DRS.

# How do we find images with internal GPS data and display them on a map to facilitate cataloging?

Using Exiftool to find all files within a directory that include  a "GPSlatitude" metadata value and write the filename out to a list, e.g., "images_with_GPS_data.txt".

        exiftool -if '$GPSlatitude ne ""' -filename -recurse -quiet -dir /media/comstock/Transcend/charliehebdo/drs_staging/* >> ~/images_with_gps_data.txt

To generate a CSV-format listing of files and associated coordinates:

		exiftool -recurse -csv -gpslatitude -gpslongitude -dir . *.tif > charlieGPS.csv

To generate a file that maps OSN to URN from the DRS deposit report.

		 awk '/JP2/ {print "http://nrs.harvard.edu/"$11"\t"$5}' Fabien_B6167982090676897383.txt > gps_urn.txt

Run CSV file (e.g., charlieGPS.csv) through [decimalDegrees.py](https://github.com/comstock/CharlieHebdo/blob/master/decimalDegrees.py) to convert the location encoding into [Decimal Degree format](https://en.wikipedia.org/wiki/Decimal_degrees), and then run the modified CSV file and the URN file (e.g., gps_urn.txt) through [URNappend.py](https://github.com/comstock/CharlieHebdo/blob/master/URNappend.py) to produce a CSV file that can be uploaded to [Google Fusion Tables](https://support.google.com/fusiontables/answer/2571232?hl=en) to create a [map showing the locations were the images were captured](https://goo.gl/cXQAcn).

# Extracting "Create Date" image technical metadata from files.
The exif Create Date field was empty on many of the CH images, but CreateDate values were extracted if available via...

'/charliehebdo/drs_staging$ exiftool -recurse -csv -createdate  -dir . *deliverable*.tif | grep -E '.*tif,[0-9]{4}.*' > ../docs/charlieHebdoCreateDate.csv'
