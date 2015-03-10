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

class SatBand(object):
    def __init__(self):
        self.data = None
        self.long_name = None
        self.dtype    = None
        self.unit = None
        self.latitude = None
        self.longitude = None

class GenericScene(object):
    def __init__(self, filepath=None, configpath=None):
        self.file_path = filepath
        self.yaml_dict = configpath
        self.bands = None
        self.longitudes = None
        self.latitudes = None
        self.area_def = None
        self.timestamp = None

    def get_filehandle(self):
        self.filehandle = open(self.file_path, 'r')

    def load(self):
        self.get_filehandle()
        self.get_bands()

    def get_coordinates(self):
        if self.area_def is None:
            self.get_area_def()
        self.longitudes, self.latitudes = self.area_def.get_lonlats()

    def resample_to_area(self, target_area_def):
        """
        Resample existing scene to the provided area definition

        """
        attributes_list_to_pass = ['bands', 'timestamp']
        resampled_scene = GenericScene()
        # resampled_scene.bands = deepcopy(self.bands)
        resampled_scene.area_def = target_area_def
        copy_attributes(self, resampled_scene, attributes_list_to_pass)

        try:
            self.area_def = geometry.SwathDefinition(lons=self.longitudes, lats=self.latitudes)
        except:
            self.get_area_def()

        valid_input_index, valid_output_index, index_array, distance_array = \
                kd_tree.get_neighbour_info(self.area_def, resampled_scene.area_def,
                                            self.area_def.pixel_size_x*2.5, neighbours = 1)

        bands_number = len(resampled_scene.bands)
        for i, band in enumerate(resampled_scene.bands.values()):
            print "Resampling band {0:d}/{1:d}".format(i+1, bands_number)
            swath_data = deepcopy(band.data)
            band.data = kd_tree.get_sample_from_neighbour_info('nn', resampled_scene.area_def.shape,
                                                                swath_data,
                                                                valid_input_index,
                                                                valid_output_index,
                                                                index_array)
        return resampled_scene

    def save_geotiff(self, filepath):
        """
        Export Scene in GeoTIFF format
        """
        self.export_path = filepath
        gtiff_driver = gdal.GetDriverByName('GTiff')
        gtiff_format = gdal.GDT_Byte
        gtiff_options = []
        bands_number = len(self.bands)
        gtiff_dataset = gtiff_driver.Create(self.export_path,
                                             int(self.area_def.x_size),
                                             int(self.area_def.y_size),
                                             bands_number,
                                             gtiff_format,
                                             gtiff_options)

        geometry_list = (self.area_def.area_extent[0],
                         self.area_def.pixel_size_x,
                         0,
                         self.area_def.area_extent[3],
                         0,
                         self.area_def.pixel_size_y * -1)

        gtiff_dataset.SetGeoTransform(geometry_list)
        srs = osr.SpatialReference()
        srs.ImportFromProj4(self.area_def.proj4_string)
        gtiff_dataset.SetProjection(srs.ExportToWkt())

        for i, band in enumerate(self.bands.values()):
            raster_array = band.data
            gtiff_dataset.GetRasterBand(i + 1).WriteArray(raster_array.astype('byte'))                    

        gtiff_dataset = None


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
                                  'lat_0': '90',
                                  'lat_ts': '60',
                                  'lon_0': '0',
                                  'ellps': 'WGS84'}

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
        self.get_bands()
        self.get_mitiff_tags()
        self.get_area_def()
        self.get_timestamp()
        # self.get_coordinates()

def load_mitiff(file_path, config_path):
    mitiff_scene = MitiffScene(file_path, config_path)
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


def copy_attributes(object_from, object_to, attributes_list):
    for attribute_name in attributes_list:
        if hasattr(object_from, attribute_name):
            the_attribute = getattr(object_from, attribute_name)
            setattr(object_to, attribute_name, deepcopy(the_attribute))

def get_area_def_from_file(area_name):
    area_filepath = get_area_filepath()
    return utils.load_area(area_filepath, area_name)

def window_blocks(large_array, window_size):
    """
    Split a large 1D array into smaller non-overlapping arrays

    Args:
      large_array (numpy.ndarray): 1d array to be split in smaller blocks
      window_size (int): window size, array shape should be divisible by this number

    Returns:
     numpy.ndarray: Resulting array with multiple small blocks of size `window_size`

    """
    y_size = large_array.shape[0]/window_size
    blocks_array = large_array.reshape(y_size, window_size)
    return blocks_array

def rescale_lac_array_to_gac(lac_array):
    """
    Create a GAC AVHRR array by averaging 4 consecutive LAC pixels
    Take only every forth scan line, omit the rest

    Args:
      lac_array (numpy.ndtype): array with scan width of 2001 pixels

    Returns:
      gac_array (numpy.ndtype): array with scan width of 400 pixels

    Note:
      Original GAC data contains 401 pixels per scanline, for the sake
      of simplicity we take only 400 pixels.

    """
    window_size = 5
    lac_array_with_omitted_lines = lac_array[::4]
    lac_array_2000px = lac_array_with_omitted_lines[:,:-1]
    flat_lac_array = lac_array_2000px.flatten()
    gac_array_flat = np.mean(window_blocks(flat_lac_array, window_size)[:,:-1], axis=1)
    gac_length = gac_array_flat.shape[0]
    gac_array_2d = gac_array_flat.reshape(gac_length/400, 400)
    return gac_array_2d
