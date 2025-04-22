# Map Tile Downloader

This Python script downloads map tiles from Thunderforest's Mobile Atlas for specified regions at multiple zoom levels. It supports resuming downloads by skipping already downloaded files and provides a progress bar to track the download progress. This was designed to make map tiles that are compatible with the Lilygo T-Deck running Ripple. 

## Features

- Download map tiles from Thunderforest's Mobile Atlas
- Specify multiple regions and zoom levels
- Skip already downloaded files
- Progress bar to track download progress
- New utility (KMLtoTiles.py) supports gross parsing of a KML,
  then fetching tiles at waypoints and routes

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library
- For KMLtoTiles: `fastkml` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/fistulareffigy/MTD-Script.git
    cd MTD-Script
    ```

2. Install the required Python packages:

    ```bash
    pip install requests tqdm
    ```

## Configuration

1. Obtain an API key from [Thunderforest](https://www.thunderforest.com/docs/apikeys/).

2. Edit the script to include your API key:

    ```python
    api_key = "your_api_key_here"
    ```

3. Specify the regions and zoom levels you want to download in the script:

    ```python
    # Define the bounding boxes and zoom levels
    regions = {
        "southern_ontario": (41.5, -83.5, 45.5, -75.0),
        "las_vegas": (35.5, -116.0, 37.5, -114.0),
        "grand_canyon": (35.5, -113.0, 37.0, -111.0)
    }
    zoom_levels = range(1, 15)  # Focusing on zoom levels 1 to 14
    ```

4. Choose map style

    ```python
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
    ```
    

   
   
## Usage (TileDL.py)

The tiles will be saved in a folder named tiles on your desktop, organized by zoom level and tile coordinates.

Run the script to start downloading tiles:

```bash
python TileDL.py
```
## Updates
2024-08-04 Thanks Scott Powell for suggesting and adding the map style selection function.

## Contributing
If you find any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details


## Usage (KMLtoTiles.py)

Run the script to start downloading tiles:

```bash
python KMLtoTiles.py <kmlfile> -k your_api_key_here -o ~/map -s outdoors -m 1000

KMLtoTiles.py [-h]
	      [-k APIKEY]
              [-s {outdoors,mobile-atlas,cycle,transport,landscape,transport-dark,spinal-map,pioneer,neighbourhood,atlas}]
	      [-m MAXTILES] [-o OUTDIR] [--minzoom MINZOOM] [--maxzoom MAXZOOM] [--latrgn LATRGN] [--lonrgn LONRGN]
	      kmlfile

Process KML file into selected tiles

positional arguments:
  kmlfile

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
  -s {outdoors,mobile-atlas,cycle,transport,landscape,transport-dark,spinal-map,pioneer,neighbourhood,atlas}, --style {outdoors,mobile-atlas,cycle,transport,landscape,transport-dark,spinal-map,pioneer,neighbourhood,atlas}
  -m MAXTILES, --maxtiles MAXTILES
  -o OUTDIR, --outdir OUTDIR
                        output directory (default: /home/ghn/maps)
  --minzoom MINZOOM     minimum zoom level
  --maxzoom MAXZOOM     maximum zoom level
  --latrgn LATRGN
  --lonrgn LONRGN

Note: zoom levels are specified as power-of-two fractions of the globe, i.e. zoom=3 means eight slices of latitude and
longitude


## Updates
2024-08-04 Thanks Scott Powell for suggesting and adding the map style selection function.

## Contributing
If you find any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details
