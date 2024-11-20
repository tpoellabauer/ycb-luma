# YCB-LUMA
Processing scripts for the YCB luminance keying test dataset for 2D object detection.

![Teaser Image](teaser.jpeg)


# Usage

Sequence of scripts to run:
0. generate_input_dirs.py (OPTIONAL)
	(ONLY NEEDED if you want to run a fresh environment without any input videos or want to create a new folders according to data.csv)
1. generate_masks.py.
	The CPU-Usage might be high. Please control your device's CPU Temperature.
2. delete_files.py
	Filters the very noisy or bad masks.
3. count.py (OPTIONAL)
	Counts the input videos and generated masks.

Description of scripts:

## generate_input_dirs.py

Description: This script will generate the needed input directories based on given data.csv.
Warning: This csv uses semicolon <;> as its delimiter.

This allows the script to find the corresponding path automatically.

The steps:
1. Edit data.csv file to add or remove directories that are going to be created.
2. run the generate_input_dirs.py
3. The folders are automatically generated on:
<name of dataset>/in/<name of generated directory>

e.g. 
data.csv contains data about:
9. Chips Can
24. Plate
71. Colored Wood Blocks (2 variations)

The generated folders are:  
|-YCB_V  
  |-in  
    |-9_chips_can  
    |-24_plate  
    |-71_1_colored_wood_blocks  
    |-71_2_colored_wood_blocks



## generate_masks.py

NOTE: Please put the videos in corresponding input folders. Name of videos do not matter.

This script generates the masks and rgb from input videos.
The output directories are also automatically generated.
Additionally, a separate csv file containing video_id and name of inputs is also generated.

e.g.:

File-name example:
For an item detected in:
frame		: 3
video		: plate_video.mp4
video_index	: 0

wil generate:

|-YCB_V
  |-out
    |-9_chips_can
      |-masks
      |-rgb
    |-24_plate
      |-masks
         |-0_frame_3.png
      |-rgb
         |-0_frame_3.png
    |-71_1_colored_wood_blocks
      |-masks
      |-rgb
    |-71_2_colored_wood_blocks
      |-masks
      |-rgb



## count.py

This script will count the number of input videos and generated masks.
The saved results will be saved based on its ID Number (for example: ID from 9_pringles_can is 9).

The results will be saved on separate csv files (with <;> as its delimiter).

e.g.
9_pringles_can:
- input videos: 4
- generated masks: 379

outputs in:
count_inputs.csv:
9; 4

count_masks.csv:
9; 379



## delete_files.py

This script will remove the output files (both in masks and rgb folder of corresponding object) that is written in files_to_delete.csv.
Note: File name doesn't have to be sorted!

Description of data entry:
directory (REQUIRED)	: name of folder, in which the data inside will be removed.  
vid_id (REQUIRED)	: the id of file that will be deleted.
				e.g. Filename: 0_frame_3.png. vid_id = 0  
from (REQUIRED)		: starting point of file index that will be removed (files with this name is included).
				e.g. Filename: 0_frame_3.png. from = 3  
to			: end point of file index that will be removed. (files with this name is included).  
			  If we want to delete a single file, fill in the "from" column and leave this one empty.
				e.g. Filename: 0_frame_6.png. to = 6

Example of an entry and its description:  
directory	  vid_id	from	to  
27_spoon	  1	      0	    231

This entry will remove masks from object "27_spoon" with filename "1_frame_0.PNG" to "1_frame_231.PNG" (and also the files between them, 1_frame_3.PNG, 1_frame_6.PNG etc)
				