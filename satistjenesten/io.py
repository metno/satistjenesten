import yaml
import collections
import numpy
import re
import datetime
import pyresample

from PIL import Image
import netCDF4 as nc
from satistjenesten import utils

class SatBand(object):
    def __init__(self):
        self.data = None
        self.long_name = None
        self.dtype    = None
        self.unit = None
        self.latitude = None
        self.longitude = None

class GenericFormat(object):
    def __init__(self, file_path, config_path):
        self.file_path = file_path
        self.yaml_dict = config_path
        self.bands = None
        self.longitudes = None
        self.latitudes = None

    def get_filehandle(self):
        self.filehandle = open(self.file_path, 'r')

    def load(self):
        self.get_filehandle()
        self.get_bands()

class Netcdf(GenericFormat):
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


class Mitiff(GenericFormat):
    def get_filehandle(self):
        self.filehandle = Image.open(self.file_path)

    def get_bands(self):
        bands = collections.OrderedDict()
        yaml_dict = utils.load_yaml_config(self.yaml_dict)
        band_dict = yaml_dict['bands']
        for (band_name, band_value) in band_dict.items():
            sat_band = SatBand()
            band_id = int(band_name)
            self.filehandle.seek(band_id)
            sat_band.data = numpy.array(self.filehandle)
            sat_band.long_name = band_value['long_name']
            bands[band_name] = sat_band
            self.filehandle.seek(0)
        self.bands = bands

    def get_area_def(self):
        tags_dict = parse_mitiff_tags()
        self.area_def = area_def_from_tags()

    def get_mitiff_tags(self):
        self.filehandle.seek(0)
        self.tags = self.filehandle.tag.tagdata
        self.parse_mitiff_tags()

    def parse_tiff_string(self, regex_pattern):
        tags_string = self.tags[270]
        regex = re.compile(regex_pattern)
        r = regex.search(tags_string)
        return r.groups()[0]


    def parse_mitiff_tags(self):
        tags_dict = {}

        satellite_pattern = "Satellite:\s(\w+([-]?\d+)?)"
        tags_dict['satellite'] = self.parse_tiff_string(satellite_pattern)

        timestamp_pattern = 'Time:\s(\d+:\d+\s\d+/\d+-\d+)'
        timestamp_string = self.parse_tiff_string(timestamp_pattern)
        datetime_timestamp = parse_mitiff_timestamp(timestamp_string)
        tags_dict['timestamp'] = datetime_timestamp

        tags_dict['proj_dict'] = {'proj': 'stere',
                                  'lat_0': 90,
                                  'lat_ts': 60,
                                  'lon_0': 0,
                                  'ellps': "WGS84"}

        # import ipdb; ipdb.set_trace() # BREAKPOINT


        xsize_pattern = 'Xsize:\s+(\d+)'
        xsize = self.parse_tiff_string(xsize_pattern)
        ysize_pattern = 'Ysize:\s+(\d+)'
        ysize = self.parse_tiff_string(ysize_pattern)

        xunit_pattern = 'Xunit:[\s+]?(\d+)'
        xunit = self.parse_tiff_string(xunit_pattern)
        yunit_pattern = 'Yunit:[\s+]?(\d+)'
        yunit = self.parse_tiff_string(yunit_pattern)

        x_px_size_pattern = 'Ax:\s(\d+\.\d+)'
        y_px_size_pattern = 'Ay:\s(\d+\.\d+)'
        x_px_size = self.parse_tiff_string(x_px_size_pattern)
        y_px_size = self.parse_tiff_string(y_px_size_pattern)

        xunit = float(xunit)
        yunit = float(yunit)

        x0_pattern = 'Bx:\s([-]?\d+\.\d+)'
        y0_pattern = 'By:\s([-]?\d+\.\d+)'
        x0 = self.parse_tiff_string(x0_pattern)
        y0 = self.parse_tiff_string(y0_pattern)

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

        area_def = pyresample.geometry.AreaDefinition('mitiff area',
                                                      'dummy area name',
                                                      'MET (diana) projection',
                                                      proj_dict,
                                                      x_size,
                                                      y_size,
                                                      area_extent)
        self.area_def = area_def

    def get_coordinates(self):
        if self.area_def is None:
            self.get_area_def()
        self.longitudes, self.latitudes = self.area_def.get_lonlats()

    def load(self):
        self.get_filehandle()
        self.get_bands()
        self.get_mitiff_tags()
        self.get_area_def()
        # self.get_coordinates()

def load_mitiff(file_path, config_path):
    mitiff_scene = Mitiff(file_path, config_path)
    mitiff_scene.load()
    return mitiff_scene

def load_netcdf(file_path, config_path):
    netcdf_scene = Netcdf(file_path, config_path)
    netcdf_scene.load()
    return netcdf_scene

def parse_mitiff_timestamp(string_timestamp):
    fmt = "%H:%M %d/%m-%Y"
    datetime_timestamp = datetime.datetime.strptime(string_timestamp, fmt)
    return datetime_timestamp
