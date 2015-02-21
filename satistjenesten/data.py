import collections
import yaml
import netCDF4
import numpy as np

from pyresample import geometry
from pyresample import kd_tree
from pyresample import utils
from pyresample import grid

from satistjenesten.utils import get_area_filepath
from satistjenesten.utils import parse_extension
from satistjenesten import io
from satistjenesten.io import SatBand


class GenericScene(object):
    """ Generic Scene object
    It is a parent class to the more customized satellite scenes

    Attributes:
      config_dict (dict): configuration dictionary that tells you how to read an input file
      config_filepath (str): file path to configuration dictionary
      scene_filepath (str): file path to input file

    """

    def __init__(self):
        self.config_dict = None
        self.config_path = None
        self.file_path = None


class SatScene(GenericScene):
    def __init__(self):
        super(SatScene, self).__init__()
        self.bands = None
        self.latitudes = None
        self.longitudes = None
        self.file_path = None
        self.config_path = None

    def load(self):
        self.file_format = parse_extension(self.file_path)
        self.load_scene(fmt=self.file_format)

    def load_scene(self, fmt=None):
        if fmt is 'mitiff':
            self.scene = io.load_mitiff(self.file_path, self.config_path)
        elif fmt is 'netcdf':
            self.scene = io.load_netcdf(self.file_path, self.config_path)
        else:
            raise Exception('{0} reader not implemented'.format(fmt))
        self.bands = self.scene.bands

    def resample_to_area(self):
        gridded_scene = GriddedSatScene()
        attributes_list_to_pass = ['bands', 'area_def', 'area_name']
        self.get_area_def()
        copy_attributes(self, gridded_scene, attributes_list_to_pass)

        try:
            self.swath_area_def = geometry.SwathDefinition(lons=self.longitudes, lats=self.latitudes)
        except:
            self.scene.get_area_def()
            self.swath_area_def = self.scene.area_def

        valid_input_index, valid_output_index, index_array, distance_array = \
                kd_tree.get_neighbour_info(self.swath_area_def, self.area_def,
                                            self.area_def.pixel_size_x*2.5, neighbours = 1)
        bands_number = len(self.bands)
        import ipdb; ipdb.set_trace() # BREAKPOINT

        for i, band in enumerate(self.bands.values()):
            print "Resampling band {0:d}/{1:d}".format(i+1, bands_number)
            swath_data = band.data.copy()
            band.data = kd_tree.get_sample_from_neighbour_info('nn', self.area_def.shape,
                                                                swath_data,
                                                                valid_input_index,
                                                                valid_output_index,
                                                                index_array)
        gridded_scene.gridded = True
        return gridded_scene

    def resample_to_gac(self):
        bands_number = len(self.bands)
        for i, band in enumerate(self.bands.values()):
            print "Resampling band {0:d} of {0:d}".format(i+1, bands_number)
            lac_data = band.data.copy()
            gac_data = rescale_lac_array_to_gac(lac_data)
            band.data = gac_data

        lac_latitudes = self.latitudes.copy()
        lac_longitudes = self.longitudes.copy()

        gac_longitudes = rescale_lac_array_to_gac(lac_longitudes)
        gac_latitudes  = rescale_lac_array_to_gac(lac_latitudes)

        self.bands['longitude'] = SatBand()
        self.bands['latitude']  = SatBand()
        self.bands['longitude'].data = gac_longitudes
        self.bands['latitude'].data  = gac_latitudes

    def get_area_def(self):
        self.area_def = get_area_def_from_file(self.area_name)


class SwathSatScene(SatScene):
    def __init__(self):
        super(SwathSatScene, self).__init__()
        self.swath_area_def = None


class GriddedSatScene(SatScene):
    def __init__(self):
        super(GriddedSatScene, self).__init__()
        self.area_name = None
        self.area_def = None
        self.gridded = False


def copy_attributes(object_from, object_to, attributes_list):
    for attribute_name in attributes_list:
        if hasattr(object_from, attribute_name):
            the_attribute = getattr(object_from, attribute_name)
            setattr(object_to, attribute_name, the_attribute)

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

