import collections
import yaml
import netCDF4

from pyresample import geometry
from pyresample import kd_tree
from pyresample import utils

from satistjenesten.utils import get_area_filepath

class GenericScene(object):
    def __init__(self):
	    self.config_dict = None
	    self.config_filepath = None
	    self.scene_filepath = None

    def parse_yaml_config(self, config_string):
	    self.config_dict = yaml.load(config_string)

    def load_config_from_file(self):
	    config_fh = open(self.config_filepath, 'r')
	    self.parse_yaml_config(config_fh)


class SatScene(GenericScene):
    def __init__(self):
	    super(SatScene, self).__init__()
	    self.bands = collections.OrderedDict()
	    self.latitudes = None
	    self.longitudes = None
	    self.input_filename = None
	    self.config_dict = None

    def get_bands(self):
	    self.bands = collections.OrderedDict()
	    band_dicts = self.config_dict['bands']
	    for (band_name, band_value) in zip(band_dicts.keys(), band_dicts.values()):
		    band = SatBand()
		    nc_dataset = get_netcdf_filehandle(self.input_filename)
		    band.data = nc_dataset.variables[band_name][:]
		    band.long_name = band_value['long_name']
		    self.bands[band_name] = band

    def get_coordinates(self):
	    nc_dataset = get_netcdf_filehandle(self.input_filename)
	    self.latitudes = nc_dataset.variables[self.config_dict['latitudes_name']][:]
	    self.longitudes = nc_dataset.variables[self.config_dict['longitudes_name']][:]

    def load_scene_from_disk(self):
	    self.load_config_from_file()
	    self.get_bands()
	    self.get_coordinates()

    def resample_to_area(self):
	    gridded_scene = GriddedSatScene()
	    attributes_list_to_pass = ['bands', 'area_def', 'area_name']
	    self.get_area_def()
	    copy_attributes(self, gridded_scene, attributes_list_to_pass)
	    # XXX: need to get radius of influence automatically
            self.swath_area_def = geometry.SwathDefinition(lons=self.longitudes,
                                                           lats=self.latitudes)
            bands_number = len(self.bands)
	    for i, band in enumerate(self.bands.values()):
                print "Resampling band {0:d}/{1:d}".format(i+1, bands_number)
		swath_data = band.data.copy()
		band.data = kd_tree.resample_nearest(self.swath_area_def,
						     swath_data,
						     self.area_def,
                                                     self.area_def.pixel_size_x,
                                                     reduce_data=True,
                                                     nprocs=2)
	    # XXX: thats ugly
	    gridded_scene.gridded = True
	    return gridded_scene

    def get_area_def(self):
	self.area_def = get_area_def_from_file(self.area_name)

    def write_as_netcdf(self):
	output_dataset = netCDF4.Dataset(self.output_filepath, 'w')

        # create dimensions
        ydim, xdim = self.bands.values()[0].data.shape
        output_dataset.createDimension('y', ydim)
        output_dataset.createDimension('x', xdim)
        output_dataset.createDimension('time', None)

        # create variables
        bands_number = len(self.bands.keys())
        for (band_name, band_object) in self.bands.items():
            variable = output_dataset.createVariable(band_name,
                                                     band_object.data.dtype, ('y', 'x'))
            variable[:] = band_object.data
	output_dataset.close()


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


class SatBand(object):
    def __init__(self):
	    self.data = None
	    self.long_name = None
	    self.dtype	= None
	    self.unit = None
	    self.latitude = None
	    self.longitude = None


def get_netcdf_filehandle(input_filename):
    return netCDF4.Dataset(input_filename, 'r')

def copy_attributes(object_from, object_to, attributes_list):
    for attribute_name in attributes_list:
	if hasattr(object_from, attribute_name):
	    the_attribute = getattr(object_from, attribute_name)
	    setattr(object_to, attribute_name, the_attribute)

def get_area_def_from_file(area_name):
    area_filepath = get_area_filepath()
    return utils.load_area(area_filepath, area_name)
