#!/usr/bin/env python
from satistjenesten import io
import argparse
import os

def make_output_filepath(input_filepath, output_dir):
    input_basename = os.path.basename(input_filepath)
    no_extension_basename = os.path.splitext(input_basename)[0]
    output_basename = "{0}.tiff".format(no_extension_basename)
    output_filepath = os.path.join(output_dir, output_basename)
    return output_filepath


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output-directory")
    p.add_argument("input_files", nargs='+',  help="Input Mitiff Files")
    p.add_argument("-c", "--channels", type=int, nargs='+', help='Channels which should be saved into geotiff')
    args = p.parse_args()

    print "Channels: ", args.channels

    files_number = len(args.input_files)
    for i, input_file in enumerate(args.input_files):
        print "Converting file {0} of {1}".format(i+1, files_number)
        output_filepath = make_output_filepath(input_file, args.output_directory)
        mitiff = io.load_mitiff(input_file)
        # mitiff.save_rgb_image('polar_lows.tif', args.channels)
        mitiff.save_geotiff(output_filepath, bands=args.channels)

if __name__ == "__main__":
    main()

