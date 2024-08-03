import os
import math
import requests
from tqdm import tqdm

API_KEY = 'Insert API key'
TILE_URL = f'Insert API URL'

# Expanded bounds for regions
REGIONS = {
    'Southern_Ontario': {
        'min_lat': 41.5, 'max_lat': 46.5,
        'min_lon': -84.5, 'max_lon': -74.5
    },
    'Las_Vegas': {
        'min_lat': 35.0, 'max_lat': 37.5,
        'min_lon': -116.5, 'max_lon': -114.0
    },
    'Grand_Canyon': {
        'min_lat': 34.0, 'max_lat': 37.0,
        'min_lon': -114.5, 'max_lon': -110.5
    }
}

OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "tiles")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def lon2tilex(lon, zoom):
    return int((lon + 180.0) / 360.0 * (1 << zoom))

def lat2tiley(lat, zoom):
    return int((1.0 - math.log(math.tan(lat * math.pi / 180.0) + 1.0 / math.cos(lat * math.pi / 180.0)) / math.pi) / 2.0 * (1 << zoom))

def download_tile(zoom, x, y):
    url = TILE_URL.format(z=zoom, x=x, y=y)
    tile_dir = os.path.join(OUTPUT_DIR, str(zoom), str(x))
    tile_path = os.path.join(tile_dir, f"{y}.png")
    os.makedirs(tile_dir, exist_ok=True)
    
    # Check if the tile already exists
    if os.path.exists(tile_path):
        print(f"Tile {zoom}/{x}/{y} already exists, skipping...")
        return
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(tile_path, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download tile {zoom}/{x}/{y}: {response.status_code} {response.reason}")

def main():
    for zoom in range(1, 15):
        for region_name, bounds in REGIONS.items():
            min_tilex = lon2tilex(bounds['min_lon'], zoom)
            max_tilex = lon2tilex(bounds['max_lon'], zoom)
            min_tiley = lat2tiley(bounds['max_lat'], zoom)  # max_lat is used here to align with top-left origin
            max_tiley = lat2tiley(bounds['min_lat'], zoom)
            
            # Create a list of (x, y) coordinates for tqdm
            tile_coords = [(x, y) for x in range(min_tilex, max_tilex + 1) for y in range(min_tiley, max_tiley + 1)]

            # Use tqdm to show progress
            for x, y in tqdm(tile_coords, desc=f"Zoom {zoom}", unit="tile"):
                download_tile(zoom, x, y)

if __name__ == "__main__":
    main()

