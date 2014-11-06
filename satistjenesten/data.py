import collections
import yaml
import netCDF4

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
		self.bands = None
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
		self.latitudes  = nc_dataset.variables[self.config_dict['latitudes_name']][:]
		self.longitudes = nc_dataset.variables[self.config_dict['longitudes_name']][:]

	def load_scene_from_disk(self):
		self.load_config_from_file()
		self.get_bands()
		self.get_coordinates()


class SwathScene(SatScene):
	def __init__(self):
		super(SwathScene, self).__init__()


class SatBand(object):
	def __init__(self):
		self.data 	= None
		self.long_name  = None
		self.dtype 	= None
		self.unit  	= None
		self.latitude 	= None
		self.longitude 	= None


def get_netcdf_filehandle(input_filename):
	return netCDF4.Dataset(input_filename, 'r')
