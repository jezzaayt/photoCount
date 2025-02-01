import os
import polars as pl 
import sys
from collections import defaultdict

def count_files(directory=".", extension=""):
    filenames = []
    for dirpath, dirnames, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                filenames.append(os.path.join(dirpath, filename))  
            
    return len(filenames), filenames  # Returns count and list of file names

if __name__ == "__main__":
    extensions = ['.raw', '.cr3', '.cr2', '.jpeg', '.png', ".jpg", ".tif", ".tiff", ".bmp", ".svg", 
    ".gif", ".mp4", ".mov", ".webp",".flv", ".mkv", ".wmv", ".m4v", ".3gp", ".mpg", ".mpeg", ".avi", ".heic", ".heif" ]
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath()
   # get directory from command line arguments
    print(directory)
    data = defaultdict(list)  # This will hold the counts and filenames for each extension
    total_count = 0
    for ext in extensions:
        count, filenames = count_files(directory, ext.upper())
        data['extension'].append(ext.strip('.'))
        data['count'].append(count)
        total_count += count
    data['percentage'] = [f'{(c/total_count)*100:.2f}%' for c in data['count']]
    print(sum(data['count']))
    df = pl.DataFrame(data)  # Create a DataFrame from the dictionary
    
    df = df.sort('count', descending=True).select(['extension', 'count', 'percentage'])
    print(df)
    df.write_csv('photo_video_count.csv')