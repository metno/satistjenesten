#!/usr/bin/env python
from satistjenesten import io
import argparse
import os
import numpy
from datetime import datetime

def make_output_filepath(input_filename, output_dir):
    output_basename = os.path.basename(input_filename)
    output_filename = os.path.join(output_dir, os.path.splitext(output_basename)[0] + '.jpg')
    return output_filename

def get_timestamp_from_filename(input_filename):
	"""
	Filename example: modis_poseidon_20150627_0755_terra_ch1-4-3.tif

	"""
        base_filename = os.path.basename(input_filename)
	date_str = base_filename.split('_')[2]
	time_str = base_filename.split('_')[3]
	timestamp = datetime.strptime('{0}_{1}'.format(date_str, time_str), '%Y%m%d_%H%M')

	return timestamp

def get_channels_combination_from_filename(input_filename):
	"""
	Filename example: modis_poseidon_20150627_0755_terra_ch1-4-3.tif
	"""
        base_filename = os.path.basename(input_filename)
	channels = base_filename.split('_')[-1]
        channels = channels.split('.')[0]
	channels_list = channels.strip('ch').split('-')
	ch1 = channels_list[0]
	ch2 = channels_list[1]
	ch3 = channels_list[2]

	channels_string = '{0}, {1}, {2}'.format(ch1, ch2, ch3)
	return channels_string

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output_dir", default='.', nargs=1)
    p.add_argument("-i", "--input-files", nargs='+',
                         help="Input MODIS input Files")

    args = p.parse_args()

    list_len = len(args.input_files)

    for i, ifile in enumerate(args.input_files):
        print "Processing file %i/%i: %s" % (i+1, list_len, os.path.basename(ifile))

        scene = io.load_geotiff(ifile)
        scene.compose_rgb_image([1, 2, 3])
        scene.add_coastlines_graticules_to_image()
        timestamp = get_timestamp_from_filename(ifile)
        timestamp_str = '{0}'.format(timestamp.isoformat())
        channel_str = get_channels_combination_from_filename(ifile)

        caption_text = u"Barents sea, MODIS, {0}, channels: {1}".format(timestamp_str, channel_str)
        scene.add_caption_to_image(caption_text)

        output_filepath = make_output_filepath(ifile, args.output_dir[0])
        scene.save_reduced_jpeg(output_filepath, 100)



    # output_filename
    # output_filepath = os.path.join(args.output_dir[0], output_filename)

if __name__ == "__main__":
    main()

