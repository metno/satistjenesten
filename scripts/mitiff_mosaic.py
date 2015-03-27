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
    p.add_argument('-c', '--channels', nargs='+',
                         help='Input channels',
                         type=int)
    p.add_argument('-a', '--area-name', nargs=1,
                         help='Name of the area definition',
                         type=str)
    p.add_argument("-i", "--input-files", nargs='+',
                         help="Input Mitiff Files")
    args = p.parse_args()

    scene_list = []

    for input_file in args.input_files:
        print "Loading %s" % (input_file)
        mitiff = io.load_mitiff(input_file, bands=args.channels)
        scene_list.append(mitiff)

    mosaic = MosaicScene()
    mosaic.get_area_def(args.area_name[0])
    mosaic.add_scenes(scene_list)
    mosaic.compose_mosaic()

    # Add '1' to channel id's for readability
    channels_string = "ch"+'-'.join(map(str, numpy.array(args.channels)+1))

    output_filename = "{}_mosaic_{}-{}_{}.tiff".format(args.satellite_name,
            mosaic.start_timestamp_string,
            mosaic.end_timestamp_string,
            channels_string)

    output_filepath = os.path.join(args.output_dir[0], output_filename)


    mosaic.save_geotiff(output_filepath, bands=args.channels)

if __name__ == "__main__":
    main()

