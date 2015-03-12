#!/usr/bin/env python
from satistjenesten import io
import argparse
import os

def make_output_filepath(input_filepath, output_dir):
    input_basename = os.path.basename(input_filepath)
    no_extension_basename = os.path.splitext(input_basename)[0]
    output_basename = "{}.tiff".format(no_extension_basename)
    output_filepath = os.path.join(output_dir, output_basename)
    return output_filepath


def main():
    p = argparse.ArgumentParser("loop_wrapper")
    p.add_argument("-o", "--output-directory")
    p.add_argument("input_files", nargs='+',  help="Input Mitiff Files")
    args = p.parse_args()

    files_number = len(args.input_files)
    for i, input_file in enumerate(args.input_files):
        print "Converting file {} of {}".format(i+1, files_number)
        output_filepath = make_output_filepath(input_file, args.output_directory)
        mitiff = io.load_mitiff(input_file)
        mitiff.save_geotiff(output_filepath)

if __name__ == "__main__":
    main()

