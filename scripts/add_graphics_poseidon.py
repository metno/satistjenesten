#!/usr/bin/env python
from satistjenesten import io
import argparse
import os
import numpy

def make_output_filepath(input_filename, output_dir):
    output_basename = os.path.basename(input_filename)
    output_filename = os.path.join(output_dir, os.path.splitext(output_basename)[0] + '.jpg')
    return output_filename

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output_dir", default='.', nargs=1)
    p.add_argument("-i", "--input-files", nargs='+',
                         help="Input MODIS input Files")

    args = p.parse_args()

    for ifile in args.input_files:
        scene = io.load_geotiff(ifile)
        scene.compose_rgb_image([1, 2, 3])
        scene.add_coastlines_graticules_to_image()
        scene.add_caption_to_image(u'Barents sea')

        output_filepath = make_output_filepath(ifile, args.output_dir[0])
        scene.save_reduced_jpeg(output_filepath, 100)



    # output_filename
    # output_filepath = os.path.join(args.output_dir[0], output_filename)

if __name__ == "__main__":
    main()

