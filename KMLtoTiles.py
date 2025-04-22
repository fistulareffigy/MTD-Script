import os
import requests
import argparse
import warnings
from pathlib import Path
from math import log, tan, cos, pi
from tqdm import tqdm
with warnings.catch_warnings():
    # This is ugly but suppresses a warning about pretty-printing we don't care about
    warnings.simplefilter('ignore')
    from fastkml import kml

from fastkml import Placemark, Point, LineString
from fastkml.utils import find_all as kml_find_all
from typing import Dict, Tuple

# Usage example:
# python KMLtoTiles.py my_input.kml -k xx_yy_your_key_here -o ~/maps/outdoors -s outdoors -m 1000

def lon2tilex(lon, zoom):
    return int((lon + 180.0) / 360.0 * (1 << zoom))

def lat2tiley(lat, zoom):
    return int((1.0 - log(tan(lat * pi / 180.0) + 1.0 / cos(lat * pi / 180.0)) / pi) / 2.0 * (1 << zoom))

def download_tile(outdir: Path, api_key: str, mapstyle: str, zoom: int, x:int, y:int):
    url = f"https://tile.thunderforest.com/{mapstyle}/{zoom}/{x}/{y}.png?apikey={api_key}"
    tile_dir = os.path.join(outdir, str(zoom), str(x))
    tile_path = os.path.join(tile_dir, f"{y}.png")
    os.makedirs(tile_dir, exist_ok=True)

    if not os.path.exists(tile_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(tile_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download tile {zoom}/{x}/{y}: {response.status_code} {response.reason}")

def expand_gps(lat, lon, latrgn, lonrgn) -> Tuple[float, float, float, float]:
    return (lat - latrgn, lon - lonrgn, lat + latrgn, lon + lonrgn)
            
def kml_to_regions(kmlfile: Path, latrgn: float = 0.1, lonrgn: float = 0.1) -> Dict[str, Tuple]:
    resdict = dict()
    k = kml.KML.parse(kmlfile)
    pmarks = list(kml_find_all(k, of_type=Placemark))
    for p in pmarks:
        pts = list(kml_find_all(p, of_type=Point))
        if len(pts) == 1:
            coords = pts[0].kml_coordinates.coords[0]
            lon = coords[0]
            lat = coords[1]
            resdict[p.name] = expand_gps(lat, lon, latrgn, lonrgn)
        else:
            coord_idx = 0
            lstrs = list(kml_find_all(p, of_type=LineString))
            for lstr in lstrs:
                for coord in lstr.kml_coordinates.coords:
                    lon = coords[0]
                    lat = coords[1]
                    name = f'{p.name}_{coord_idx:06}'
                    resdict[name] = expand_gps(lat, lon, latrgn, lonrgn)
                    coord_idx += 1
    return resdict

def download_tiles(regions: Dict[str, Tuple],
                   outdir: Path, apikey: str,
                   mapstyle: str, maxtiles: int,
                   minzoom: int = 1, maxzoom: int = 12):
    fetch = set()
    nofetch = set()
    highest_zoom = None

    print('Iterating zoom levels: ', end='')
    for zoom in range(minzoom, maxzoom+1):
        print(f'{zoom}...', end='', flush=True)
        for min_lat, min_lon, max_lat, max_lon in regions.values():
            start_x = lon2tilex(min_lon, zoom)
            end_x = lon2tilex(max_lon, zoom)
            start_y = lat2tiley(max_lat, zoom)
            end_y = lat2tiley(min_lat, zoom)

            tba = (end_x - start_x + 1) * (end_y - start_y + 1)
            if len(fetch) + tba < maxtiles:
                highest_zoom = zoom
                for x in range(start_x, end_x + 1):
                    for y in range(start_y, end_y + 1):
                        fetch.add((zoom, x, y))
            else:
                for x in range(start_x, end_x + 1):
                    for y in range(start_y, end_y + 1):
                        nofetch.add((zoom, x, y))

    print()
    fetch_count = len(fetch)
    total_count = len(fetch) + len(nofetch)
    print(f'Fetching {fetch_count} tiles out of requested {total_count}')
    print(f'Highest zoom level included is {highest_zoom}')
    
    with tqdm(total=fetch_count, desc="Downloading tiles") as pbar:
        for (zoom, x, y) in fetch:
            download_tile(outdir, apikey, mapstyle, zoom, x, y)
            pbar.update(1)

if __name__ == "__main__":
    def_out = os.path.join(os.path.expanduser("~"), "maps")
    p = argparse.ArgumentParser(
        prog='KMLtoTiles.py',
        description='Process KML file into selected tiles',
        epilog='''
Note: zoom levels are specified as power-of-two fractions of the\n
globe, i.e. zoom=3 means eight slices of latitude and longitude
'''
    )
    p.add_argument('kmlfile', type=Path)
    p.add_argument('-k', '--apikey', type=str, required=True)
    p.add_argument('-s', '--style', type=str, default='outdoors',
                   choices=['outdoors', 'mobile-atlas', 'cycle',
                            'transport', 'landscape', 'transport-dark',
                            'spinal-map', 'pioneer', 'neighbourhood', 'atlas'])
    p.add_argument('-m', '--maxtiles', type=int, default=1000)
    p.add_argument('-o', '--outdir', type=Path,
                   default = def_out,
                   help = 'output directory (default: %(default)s)')
    p.add_argument('--minzoom', type=int, default=1,
                   help = 'minimum zoom level')
    p.add_argument('--maxzoom', type=int, default=15,
                   help = 'maximum zoom level')
    p.add_argument('--latrgn', type=float, default=0.1)
    p.add_argument('--lonrgn', type=float, default=0.1)

    args = p.parse_args()
    regions = kml_to_regions(args.kmlfile,
                             latrgn=args.latrgn,
                             lonrgn=args.lonrgn,
    )

    os.makedirs(args.outdir, exist_ok=True)
    download_tiles(regions,
                   apikey=args.apikey,
                   outdir=args.outdir,
                   mapstyle=args.style,
                   maxtiles=args.maxtiles,
                   minzoom=args.minzoom,
                   maxzoom=args.maxzoom,
    )
