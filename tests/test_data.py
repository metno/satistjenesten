import unittest
from satistjenesten import data

config_string = """
channels:
  channel_1:
    name: reflec_1
"""

class TestScene(unittest.TestCase):
	def setUp(self):
		self.scene = data.SatScene()
		self.scene.input_filename = 'test_data/metop-b.nc'
		self.config_filepath = 'test_data/test_config.yml'
	
	def test_VanillaSceneObject_HasNoConfig(self):
		self.assertIsNone(self.scene.config_dict)
	
	def test_Scene_ParsesYamlConfig(self):
		expected_dict = {'name': 'reflec_1'}
		self.scene.parse_yaml_config(config_string)
		self.assertDictEqual(self.scene.config_dict['channels']['channel_1'], expected_dict)

	def test_Scene_LoadsYamlConfig_FromFile(self):
		self.scene.load_config_from_file(self.config_filepath)

	def test_Scene_LoadsScene_FromFile(self):
		self.scene.load_scene_from_file()
