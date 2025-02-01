# Photo and Video File Counting Script


This Python script is designed to count the number of different photo (image) and video file formats within a specified directory, providing both the total count and a breakdown by extension type. The results are then saved as a CSV file for easy analysis or further processing.

# Usage:
Run countPhoto.py [directory] in your command line interface (CLI). If no directory is specified, it defaults to the current working directory.
It will print out each extension type and its count in descending order.
At the end, a CSV file named 'photo_video_count.csv' will be created with the same information in tabular format for easy viewing or further analysis.
# Features:
Counts the following image and video formats in the specified directory: 
- JPEG
- PNG
- CR2
- CR3
- RAW
- TIFF
- BMP
- SVG
- GIF
- MP4
- MOV
- WEBP
- FLV
- MKV
- WMV
- M4V
- 3GP
- MPG
- MPEG
- AVI
- HEIC
- HEIF

# Output:
The script will print out each extension type and its count in descending order.
It will also print out the total count of all files found.

# Example Output:

```
Directory: .
Total count: 729225
JPEG: 72910
CR2: 100
PNG: 13
CR3: 2
RAW: 0
TIFF: 0
BMP: 0
SVG: 0
GIF: 0
MP4: 0
MOV: 0
WEBP: 0
FLV: 0
MKV: 0
WMV: 0
M4V: 0
3GP: 0
MPG: 0
MPEG: 0
AVI: 0
HEIC: 0
HEIF: 0
```
Calculates the percentage of total file count for each extension.
Saves results in a CSV file 'photo_video_count.csv' for easy viewing or further analysis.
Uses the polars library to create and manage DataFrames, providing efficient and memory-friendly operations.
