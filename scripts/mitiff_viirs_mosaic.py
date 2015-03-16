#!/usr/bin/env python
from satistjenesten import io
from satistjenesten.mosaic import MosaicScene
import argparse
import os

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output-file")
    p.add_argument("input_files", nargs='+',  help="Input Mitiff Files")
    args = p.parse_args()

    scene_list = []
    bands_list = [4, 3, 2]

    files_number = len(args.input_files)
    for i, input_file in enumerate(args.input_files):
        mitiff = io.load_mitiff(input_file, bands=bands_list)
        scene_list.append(mitiff)

    mosaic = MosaicScene()
    mosaic.get_area_def('istjenesten_main_1k')
    mosaic.add_scenes(scene_list)
    mosaic.compose_mosaic()
    mosaic.save_geotiff(args.output_file, bands=bands_list)

if __name__ == "__main__":
    main()

