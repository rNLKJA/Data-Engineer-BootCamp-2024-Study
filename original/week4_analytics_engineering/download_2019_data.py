"""
Download Yellow and Green taxi data for 2019 (July only for Q4)
"""
import requests
import os
from pathlib import Path

def download_file(url, dest_path):
    """Download a file from URL to dest_path"""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    file_size = os.path.getsize(dest_path) / (1024 * 1024)
    print(f"  Downloaded: {dest_path.name} ({file_size:.1f} MB)")

def main():
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    # Create directories
    yellow_dir = Path("data/yellow_2019")
    green_dir = Path("data/green_2019")
    yellow_dir.mkdir(parents=True, exist_ok=True)
    green_dir.mkdir(parents=True, exist_ok=True)

    # Download July 2019 data (needed for Q4)
    files_to_download = [
        ("yellow_tripdata_2019-07.parquet", yellow_dir),
        ("green_tripdata_2019-07.parquet", green_dir),
    ]

    for filename, target_dir in files_to_download:
        dest_path = target_dir / filename
        if dest_path.exists():
            print(f"Skipping {filename} (already exists)")
            continue

        url = f"{base_url}/{filename}"
        try:
            download_file(url, dest_path)
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nDownload complete!")

if __name__ == "__main__":
    main()
