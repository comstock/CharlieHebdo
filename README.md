# CharlieHebdo
scripts used to process the CH collection for DRS depositing

1) create a list of all files in CH filesystem
2) run program that...
* finds the filetypes you plan to move to DRS
* creates a drs staging area for the files
* generates drs-friendly folder and filenames
* generates a list of orig paths + filenames and new paths + filenames (so archivists can trace deposited to original files)
* performs some format validation
* generates a list of all files not processed for deposit, because they fail to meet our target criteria (e.g., only jpgs, tiffs, and pngs).
* generates a list of all files that fail validation and are therefore not copied to drs staging area.
* copies over original file to staging area within "master" directory in case these can be deposited.

3) run imperfect script to embed original filenames in exif metadata of the copied files (script fails for small number of files)

4) run script that generates TIFF files from all of the copied image files and deletes the non-TIFF copy from staging area

* maybe re-run exiftool origFileName script on TIFFs, in case the failures were PNG-specifc

5) run script that copies all consent forms over to drs staging area
* revise script to create "license" folders within each donor folder, and to deposit the licenses w/in.

======

# Notes on icc profile script

# what data would you need to pass to and return from a module?

* input filename prefix (newNameStub)
* input filename suffix (file_ext)
* input filename path (copypath)
* destination sRGB profile path and name (srgb_link)
* path where you would write to and call your link (input-icc-TO-output-icc) profile
* path where you would write your output file (copypath)

# Using ARGYLL software to perform a profile-to-profile conversion. #

1) generate a profile that maps between the source and destination colorspace:

* collink -v -ip ./icc_input.tif ./sRGB.icm ./icc_input.icm

# Note that collink will extract the profile embedded in ./icc_input.tif. If I had the source profile as a descrete file (e.g., ./icc_input.icm), I could referenced the profile instead of the image that contains the source profile.

* ./sRGB.icm is the destination profile.

* ./icc_input.icm is the input.icm-TO-output.icm profile.

* 2) generate a correctly derived (from icc_input.tif) sRGB icc_output_srgb.tif file.

* cctiff -v -ip ./icc_input.icm -e ./sRGB.icm ./icc_input.tif icc_output_srgb.tif
