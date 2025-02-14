import os 
import polars as pl
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
def count_files(directory=".", extension=""):
    try:
        filenames = []
        for dirpath, dirnames, files in os.walk(directory):
            for filename in files:
                if filename.endswith(extension) or filename.endswith(extension.upper()):
                    filenames.append(os.path.join(dirpath, filename))

        return len(filenames), filenames  # Returns count and list of file names
    except Exception as e:
        logging.error(f"Error counting files: {e}")
        return 0, []

def parse_args():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.abspath(".")
    if len(sys.argv) > 2:
        output_csv = sys.argv[2]
    else:
        output_csv = 'photo_video_count.csv'
    
    extensions = ['.raw', '.cr3', '.cr2', '.jpeg', '.png', ".jpg", ".tif", ".tiff", ".bmp", ".svg", 
    ".gif", ".mp4", ".mov", ".webp",".flv", ".mkv", ".wmv", ".m4v", ".3gp", ".mpg", ".mpeg", ".avi", ".heic", ".heif", ".json"] # list of extensions to count 
    # JSON is here as Google Photo exports includes that as part of some photos 
    return directory, extensions, output_csv


def plot_count(df):
 
    fig, ax = plt.subplots()
    ax.scatter(df['extension'], df['count']) 
    ax.set_xlabel('Extensions')
    ax.set_ylabel('Count')
    ax.set_title('Scatter plot of Extension by Count')
    # Add text labels for each point in the scatter plot
    for i, txt in enumerate(df['count']):
        ax.annotate(txt, (df['extension'][i], df['count'][i]))
    # Set y-axis limits to include all data points within a certain range
    ax.set_ylim([0, max(df['count']) * 1.2]) # multiply by 1.2 for a bit of extra space at the top
    fig.savefig('scatter_plot.png', dpi= 300)

def main(directory, extensions, output_csv):
    # Check that the directory exists
    if not os.path.exists(directory):
        logging.error(f"Directory {directory} does not exist")
        return 0, []

    extension_counts = pl.DataFrame({
        'filename': [],
        'extension': []
    })

    file_list = []
    

    for ext in tqdm(extensions, desc="Counting files"):
        count, filenames = count_files(directory, ext.strip('.'))

        
        if count > 0:
            file_list.extend(filenames)
    # Create a DataFrame from the list of file names
    df = pl.DataFrame({
        'filename': file_list,
        'extension': [os.path.splitext(filename)[1][1:] for filename in file_list]

    })
    print(df)
    # Aggregate and count unique extensions
    extension_counts = (
        df.lazy()
        .group_by('extension')
        .agg(pl.len().alias('count'))
        .sort('count', descending=True)
        .filter(pl.col("count") > 0)
        .collect()
    )

    print(f"Total files found: {sum(extension_counts['count'])}")
    
    extension_counts.write_csv(output_csv)
    if not extension_counts.is_empty():
        plot_count(extension_counts)
    return extension_counts


def plot_count(df):
    fig, ax = plt.subplots()
    ax.bar(df['extension'], df['count'])
    ax.set_xlabel('Extensions')
    ax.set_ylabel('Count')
    ax.set_title('Bar Plot of File Extensions by Count')
    
    for i, count in enumerate(df['count']):
        ax.text(i, count + 50, str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('scatter_plot.png', dpi=300)

if __name__ == "__main__":
    directory = os.path.abspath('.')
    extensions = ['.raw', '.cr3', '.cr2', '.jpeg', '.png', ".jpg", ".tif", ".tiff", ".bmp", ".svg",
                  ".gif", ".mp4", ".mov", ".webp", ".flv", ".mkv", ".wmv", ".m4v", ".3gp", ".mpg",
                  ".mpeg", ".avi", ".heic", ".heif", ".json"]
    directory, extensions, output_csv = parse_args()
    main(directory, extensions, output_csv)
