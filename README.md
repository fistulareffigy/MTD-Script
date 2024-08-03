# Map Tile Downloader

This Python script downloads map tiles from Thunderforest's Mobile Atlas for specified regions at multiple zoom levels. It supports resuming downloads by skipping already downloaded files and provides a progress bar to track the download progress.

## Features

- Download map tiles from Thunderforest's Mobile Atlas
- Specify multiple regions and zoom levels
- Skip already downloaded files
- Progress bar to track download progress

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library

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

## Usage

Run the script to start downloading tiles:

```bash
python TileDL.py
