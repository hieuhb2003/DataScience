import os
import wget
import zipfile
from pathlib import Path

def download_data():
    # Create data and models directories
    Path('data').mkdir(exist_ok=True)
    
    # Download CSV file
    print("Downloading CSV file...")
    wget.download(
        'https://huggingface.co/datasets/meandyou200175/btl_khdl/resolve/main/output_file.csv',
        'data/output_file.csv'
    )
    
    print("\nDownload complete!")

if __name__ == "__main__":
    download_data()