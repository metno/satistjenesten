import yaml

class SatScene(object):
	def __init__(self):
		self.config_dict = None
		self.config_filepath = None
		self.scene_filepath = None

	def parse_yaml_config(self, config_string):
		self.config_dict = yaml.load(config_string)

	def load_config_from_file(self):
		pass

	def load_scene_from_file():
		pass
