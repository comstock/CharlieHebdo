# CharlieHebdo
scripts used to process the CH collection for DRS depositing

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
