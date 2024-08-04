import os
import requests
from math import log, tan, cos, pi
from tqdm import tqdm

# Define the bounding boxes and zoom levels. Below are random examples.
regions = {
    "southern_ontario": (41.5, -83.5, 45.5, -75.0),
    "las_vegas": (35.5, -116.0, 37.5, -114.0),
    "grand_canyon": (35.5, -113.0, 37.0, -111.0)
}
zoom_levels = range(1, 15)  # Focusing on zoom levels 1 to 14

# mapstyle = "cycle"
# mapstyle = "transport"
# mapstyle = "landscape"
# mapstyle = "outdoors"
# mapstyle = "transport-dark"
# mapstyle = "spinal-map"
# mapstyle = "pioneer"
mapstyle = "mobile-atlas"
# mapstyle = "neighbourhood"
# mapstyle = "atlas"

# API Key and output directory
api_key = "your_api_key_here"
output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "tiles")
os.makedirs(output_dir, exist_ok=True)

def lon2tilex(lon, zoom):
    return int((lon + 180.0) / 360.0 * (1 << zoom))

def lat2tiley(lat, zoom):
    return int((1.0 - log(tan(lat * pi / 180.0) + 1.0 / cos(lat * pi / 180.0)) / pi) / 2.0 * (1 << zoom))

def download_tile(zoom, x, y):
    url = f"https://tile.thunderforest.com/{mapstyle}/{zoom}/{x}/{y}.png?apikey={api_key}"
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
