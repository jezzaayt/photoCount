import os
import polars as pl 
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import time

def count_files(directory=".", extension=""):
    filenames = []
    for dirpath, dirnames, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension) or filename.endswith(extension.upper()):
                filenames.append(os.path.join(dirpath, filename))

    return len(filenames), filenames  # Returns count and list of file names

if __name__ == "__main__":
    extensions = ['.raw', '.cr3', '.cr2', '.jpeg', '.png', ".jpg", ".tif", ".tiff", ".bmp", ".svg", 
    ".gif", ".mp4", ".mov", ".webp",".flv", ".mkv", ".wmv", ".m4v", ".3gp", ".mpg", ".mpeg", ".avi", ".heic", ".heif", ".json"]
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(".")
   # get directory from command line arguments
    print(directory)
    data = defaultdict(list)  # This will hold the counts and filenames for each extension
    total_count = 0
    for ext in extensions:
        count, filenames = count_files(directory, ext)
        data['extension'].append(ext.strip('.'))
        data['count'].append(count)
        total_count += count
    try:
        data['percentage'] = [f'{(c/total_count)*100:.2f}%' for c in data['count']] 
    except ZeroDivisionError:
        data['percentage'] = [f'{0:.2f}%' for c in data['count']]
    print(sum(data['count']))
    df = pl.DataFrame(data)  # Create a DataFrame from the dictionary
    
    df = df.sort('count', descending=True).select(['extension', 'count', 'percentage'])
    print(df)
    df.write_csv('photo_video_count.csv')
    if len(df) > 0:
        filtered_df = df.filter(pl.col("count") > 0)


        fig, ax = plt.subplots()
    
     
        ax.scatter(filtered_df['extension'], filtered_df['count']) 
        ax.set_xlabel('Extensions')
        ax.set_ylabel('Count')
        ax.set_title('Scatter plot of Extension by Count')

        # Add text labels for each point in the scatter plot
        for i, txt in enumerate(filtered_df['count']):
            ax.annotate(txt, (filtered_df['extension'][i], filtered_df['count'][i]))
        
        # Set y-axis limits to include all data points within a certain range
        ax.set_ylim([0, max(filtered_df['count']) * 1.2]) # multiply by 1.2 for a bit of extra space at the top

        fig.savefig('scatter_plot.png', dpi= 300) 
        