#!/usr/bin/env python
import sys
from satistjenesten import io
from pyresample import utils
import argparse
input_file = sys.argv[1]
config_file = sys.argv[2]
output_gtiff_file = sys.argv[3]

new_area_def = utils.load_area('areas.cfg', 'istjenesten_main_4k')
mitiff = io.load_mitiff(input_file)
mitiff.save_geotiff(output_gtiff_file)
