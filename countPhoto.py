import os 
import polars as pl
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def count_files(directory=".", extensions=None):
    if extensions is None:
        extensions = ['.raw', '.cr3', '.cr2', '.jpeg', '.png', ".jpg", ".tif", ".tiff", ".bmp", ".svg", 
                      ".gif", ".mp4", ".mov", ".webp", ".flv", ".mkv", ".wmv", ".m4v", ".3gp", ".mpg", 
                      ".mpeg", ".avi", ".heic", ".heif", ".json"]

    if not os.path.exists(directory):
        logging.error(f"Directory {directory} does not exist")
        return 0, []

    extension_counts = pl.DataFrame({
        'filename': [],
        'extension': []
    })

    for ext in tqdm(extensions, desc="Counting files"):
        count = (
            pl.scan_paths(
                os.path.join(directory, "**/*." + ext),
                projection="filename"
            )
            .with_column(pl.col('filename').str.extract(r'.*/([^/]+)$').alias('filename'))
            .with_column(pl.col('filename').str.slice(-len(ext), None).str.strip('.').alias('extension'))
            .group_by("extension")
            .agg([pl.count().alias('count')])
            .collect()
        )

        if count.shape[0] > 0:
            extension_counts = extension_counts.vstack(count)

    total_count = sum(extension_counts.get_column('count'))
    percentage_df = (
        extension_counts
        .with_columns(
            pl.col('count').map_elements(lambda x: f'{(x/total_count)*100:.3f}%', return_dtype=pl.Utf8).alias('percentage')
        )
        .filter(pl.col("count") > 0)
    )

    print(f"Total files found: {sum(extension_counts['count'])}")
    print(percentage_df)

    if not percentage_df.is_empty():
        percentage_df.write_csv('photo_video_count.csv')

    return percentage_df

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

    percentage_df = count_files(directory, extensions)
    
    if not percentage_df.is_empty():
        plot_count(percentage_df)
