import yaml
import collections
import numpy

from PIL import Image
import netCDF4 as nc

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

class NetCdf(GenericFormat):
    def get_filehandle(self):
        self.filehandle = nc.Dataset(self.file_path, 'r')

    def get_bands(self):
        bands = collections.OrderedDict()
        yaml_dict = load_yaml_config(self.yaml_dict)
        band_dict = yaml_dict['bands']
        for (band_name, band_value) in band_dict.items():
            sat_band = SatBand()
            sat_band.data = self.filehandle['band_name'][:]
            sat_band.long_name = band_value['long_name']
            bands[band_name] = sat_band
        self.bands = bands


class Mitiff(GenericFormat):
    def get_filehandle(self):
        self.filehandle = Image.open(self.file_path)
    
    def get_bands(self):
        bands = collections.OrderedDict()
        yaml_dict = load_yaml_config(self.yaml_dict)
        band_dict = yaml_dict['bands']
        for (band_name, band_value) in band_dict.items():
            sat_band = SatBand()
            band_id = int(band_name)
            self.filehandle.seek(band_id)
            sat_band.data = numpy.array(self.image)
            sat_band.long_name = band_value['long_name']
            bands[band_name] = sat_band
        self.bands = bands

def load_mitiff(file_path, config_path):
    mitiff_scene = Mitiff(file_path, config_path)
    mitiff_scene.load()
    return mitiff_scene

def load_netcdf(file_path, config_path):
    netcdf_scene = Netcdf(file_path, config_path)
    netcdf_scene.load()
    return netcdf_scene
