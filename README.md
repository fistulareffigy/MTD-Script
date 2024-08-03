Map Tile Downloader
This Python script downloads map tiles from Thunderforest's Mobile Atlas for specified regions at multiple zoom levels. It supports resuming downloads by skipping already downloaded files and provides a progress bar to track the download progress.

Features
Download map tiles from Thunderforest's Mobile Atlas
Specify multiple regions and zoom levels
Skip already downloaded files
Progress bar to track download progress
Requirements
Python 3.x
requests library
tqdm library
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/map-tile-downloader.git
cd map-tile-downloader
Install the required Python packages:

bash
Copy code
pip install requests tqdm
Configuration
Obtain an API key from Thunderforest.

Edit the script to include your API key:

python
Copy code
api_key = "your_api_key_here"
Specify the regions and zoom levels you want to download in the script:

python
Copy code
# Define the bounding boxes and zoom levels
regions = {
    "southern_ontario": (41.5, -83.5, 45.5, -75.0),
    "las_vegas": (35.5, -116.0, 37.5, -114.0),
    "grand_canyon": (35.5, -113.0, 37.0, -111.0)
}
zoom_levels = range(1, 15)  # Focusing on zoom levels 1 to 14
Usage
Run the script to start downloading tiles:

bash
Copy code
python tile_downloader.py
The tiles will be saved in a folder named tiles on your desktop, organized by zoom level and tile coordinates.

Script
Here is the complete script:

python
Copy code
import os
import requests
from math import log, tan, cos, pi
from tqdm import tqdm

# Define the bounding boxes and zoom levels
regions = {
    "southern_ontario": (41.5, -83.5, 45.5, -75.0),
    "las_vegas": (35.5, -116.0, 37.5, -114.0),
    "grand_canyon": (35.5, -113.0, 37.0, -111.0)
}
zoom_levels = range(1, 15)  # Focusing on zoom levels 1 to 14

# API Key and output directory
api_key = "your_api_key_here"
output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "tiles")
os.makedirs(output_dir, exist_ok=True)

def lon2tilex(lon, zoom):
    return int((lon + 180.0) / 360.0 * (1 << zoom))

def lat2tiley(lat, zoom):
    return int((1.0 - log(tan(lat * pi / 180.0) + 1.0 / cos(lat * pi / 180.0)) / pi) / 2.0 * (1 << zoom))

def download_tile(zoom, x, y):
    url = f"https://tile.thunderforest.com/mobile-atlas/{zoom}/{x}/{y}.png?apikey={api_key}"
    tile_dir = os.path.join(output_dir, str(zoom), str(x))
    tile_path = os.path.join(tile_dir, f"{y}.png")
    os.makedirs(tile_dir, exist_ok=True)

    if not os.path.exists(tile_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(tile_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download tile {zoom}/{x}/{y}: {response.status_code} {response.reason}")

def main():
    total_tiles = 0

    for zoom in zoom_levels:
        for min_lat, min_lon, max_lat, max_lon in regions.values():
            start_x = lon2tilex(min_lon, zoom)
            end_x = lon2tilex(max_lon, zoom)
            start_y = lat2tiley(max_lat, zoom)
            end_y = lat2tiley(min_lat, zoom)

            total_tiles += (end_x - start_x + 1) * (end_y - start_y + 1)

    with tqdm(total=total_tiles, desc="Downloading tiles") as pbar:
        for zoom in zoom_levels:
            for min_lat, min_lon, max_lat, max_lon in regions.values():
                start_x = lon2tilex(min_lon, zoom)
                end_x = lon2tilex(max_lon, zoom)
                start_y = lat2tiley(max_lat, zoom)
                end_y = lat2tiley(min_lat, zoom)

                for x in range(start_x, end_x + 1):
                    for y in range(start_y, end_y + 1):
                        download_tile(zoom, x, y)
                        pbar.update(1)

if __name__ == "__main__":
    main()
Contributing
If you find any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

