import yaml
import collections
import numpy
import re
import datetime
from copy import copy, deepcopy
from osgeo import gdal, osr

from pyresample import geometry
from pyresample import kd_tree
from PIL import Image
import netCDF4 as nc
from satistjenesten import utils
from satistjenesten.scene import GenericScene, SatBand

class NetcdfScene(GenericScene):
    def get_filehandle(self):
        self.filehandle = nc.Dataset(self.file_path, 'r')

    def get_bands(self):
        bands = collections.OrderedDict()
        yaml_dict = utils.load_yaml_config(self.yaml_dict)
        band_dict = yaml_dict['bands']
        for (band_name, band_value) in band_dict.items():
            sat_band = SatBand()
            sat_band.data = self.filehandle.variables[band_name][:]
            sat_band.long_name = band_value['long_name']
            bands[band_name] = sat_band
        self.bands = bands

class MitiffScene(GenericScene):
    def get_filehandle(self):
        self.filehandle = Image.open(self.file_path)

    def get_bands(self):
        bands_dict = collections.OrderedDict()
        bands_number = int(self.tags_dict['channels_number'])

        bands_list = None

        try:
            bands_list = self.kwargs['bands']
        except:
            bands_list = range(bands_number)

        bands_number = len(bands_list)

        for band in bands_list:
            sat_band = SatBand()
            band_id = band
            self.filehandle.seek(band_id)
            sat_band.data = numpy.array(self.filehandle)
            bands_dict[band_id] = sat_band
        self.bands = bands_dict

    def get_area_def(self):
        tags_dict = parse_mitiff_tags()
        self.area_def = area_def_from_tags()

    def get_mitiff_tags(self):
        self.filehandle.seek(0)
        self.tags = self.filehandle.tag.tagdata
        self.parse_mitiff_tags()

    def parse_tag_string(self, regex_pattern):
        tags_string = self.tags[270]
        regex = re.compile(regex_pattern)
        r = regex.search(tags_string)
        return r.groups()[0]

    def parse_mitiff_tags(self):
        tags_dict = {}

        satellite_pattern = "Satellite:\s(\w+([-]?\d+)?)"
        tags_dict['satellite'] = self.parse_tag_string(satellite_pattern)

        channels_number_pattern = "Channels:\s+(\d+)"
        channels_number = self.parse_tag_string(channels_number_pattern)

        # XXX: Dirty fix -- there is a bug in NOAA avhrr Mitiff files
        # where the channel number is 9 instead of 6
        # If we encounter files with 9 channels let's assume it should be 6
        if channels_number == '9':
            channels_number = '6'

        tags_dict['channels_number'] = channels_number

        timestamp_pattern = 'Time:\s(\d+:\d+\s\d+/\d+-\d+)'
        timestamp_string = self.parse_tag_string(timestamp_pattern)
        datetime_timestamp = parse_mitiff_timestamp(timestamp_string)
        tags_dict['timestamp'] = datetime_timestamp

        proj_string_pattern = 'Proj string:\s(.*)\n'
        tags_dict['proj_dict'] = {'proj': 'stere',
                                  'lat_0': '90',
                                  'lat_ts': '60',
                                  'lon_0': '0',
                                  'ellps': 'WGS84'}

        xsize_pattern = 'Xsize:\s+(\d+)'
        xsize = self.parse_tag_string(xsize_pattern)
        ysize_pattern = 'Ysize:\s+(\d+)'
        ysize = self.parse_tag_string(ysize_pattern)

        xunit_pattern = 'Xunit:[\s+]?(\d+)'
        xunit = self.parse_tag_string(xunit_pattern)
        yunit_pattern = 'Yunit:[\s+]?(\d+)'
        yunit = self.parse_tag_string(yunit_pattern)

        x_px_size_pattern = 'Ax:\s(\d+\.\d+)'
        y_px_size_pattern = 'Ay:\s(\d+\.\d+)'
        x_px_size = self.parse_tag_string(x_px_size_pattern)
        y_px_size = self.parse_tag_string(y_px_size_pattern)

        xunit = float(xunit)
        yunit = float(yunit)

        x0_pattern = 'Bx:\s([-]?\d+\.\d+)'
        y0_pattern = 'By:\s([-]?\d+\.\d+)'
        x0 = self.parse_tag_string(x0_pattern)
        y0 = self.parse_tag_string(y0_pattern)

        tags_dict['x0'] = float(x0) * xunit
        tags_dict['y0'] = float(y0) * xunit
        tags_dict['x_px_size'] = float(x_px_size) * xunit
        tags_dict['y_px_size'] = float(y_px_size) * yunit
        tags_dict['xsize'] = float(xsize)
        tags_dict['ysize'] = float(ysize)

        self.tags_dict = tags_dict

    def get_timestamp(self):
        if self.tags_dict:
            self.timestamp = self.tags_dict['timestamp']

    def get_area_def(self):
        tags = self.tags_dict

        if tags is None:
            raise Exception('No meta data available')

        proj_dict = tags['proj_dict']

        x_size = tags['xsize']
        y_size = tags['ysize']
        x_px_size = tags['x_px_size']
        y_px_size = tags['y_px_size']

        x_ul_corner = tags['x0']
        y_ul_corner = tags['y0']
        x_ur_corner = x_ul_corner + x_size * x_px_size
        y_ur_corner = y_ul_corner
        x_ll_corner = x_ul_corner
        y_ll_corner = y_ul_corner - y_size * y_px_size
        area_extent = (x_ll_corner, y_ll_corner, x_ur_corner, y_ur_corner)

        area_def = geometry.AreaDefinition('mitiff area',
                                           'dummy area name',
                                           'MET (diana) projection',
                                           proj_dict,
                                           x_size,
                                           y_size,
                                           area_extent)
        self.area_def = area_def

    def load(self):
        self.get_filehandle()
        self.get_mitiff_tags()
        self.get_bands()
        self.get_area_def()
        self.get_timestamp()

def load_mitiff(file_path, **kwargs):
    mitiff_scene = MitiffScene(filepath=file_path, **kwargs)
    mitiff_scene.load()
    return mitiff_scene

def load_netcdf(file_path, config_path):
    netcdf_scene = NetcdfScene(file_path, config_path)
    netcdf_scene.load()
    return netcdf_scene

def parse_mitiff_timestamp(string_timestamp):
    fmt = "%H:%M %d/%m-%Y"
    datetime_timestamp = datetime.datetime.strptime(string_timestamp, fmt)
    return datetime_timestamp


def get_area_def_from_file(area_name):
    area_filepath = get_area_filepath()
    return utils.load_area(area_filepath, area_name)


