#!/usr/bin/env python
from satistjenesten import io
from satistjenesten.mosaic import MosaicScene
import argparse
import os
import numpy

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--satellite_name")
    p.add_argument("-o", "--output_dir", default='.', nargs=1)
    p.add_argument('-b', '--channels', nargs='+',
                         help='Input channels',
                         type=str)
    p.add_argument('-a', '--area-name', nargs=1,
                         help='Name of the area definition',
                         type=str)
    p.add_argument("-i", "--input-files", nargs='+',
                         help="Input Mitiff Files")
    args = p.parse_args()

    scene_list = []

    for input_file in args.input_files:
        print "Loading %s" % (input_file)
        amsr2_scene = io.load_osisaf_amsr2_netcdf(input_file, bands=args.channels)
        scene_list.append(amsr2_scene)

    mosaic = MosaicScene()
    mosaic.get_area_def(args.area_name[0])
    mosaic.compose_mosaic(scene_list, resample_method='gaussian')

    output_filename = "{0}_12hr-mosaic_{1}.tiff".format(args.satellite_name,
            mosaic.end_timestamp_string)

    output_filepath = os.path.join(args.output_dir[0], output_filename)


    mosaic.save_geotiff(output_filepath, bands=args.channels, cmap='istjenesten')

if __name__ == "__main__":
    main()

