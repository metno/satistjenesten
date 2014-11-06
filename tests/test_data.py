import unittest
import tempfile
import yaml
import os

from satistjenesten import data

config_string = """
bands:
  reflec_1:
    long_name: reflectivity
"""

class TestScene(unittest.TestCase):
	def setUp(self):
		self.scene = data.SatScene()
		self.input_filename = 'test_data/metop-b.nc'
	
	def test_VanillaSceneObject_HasNoConfig(self):
		self.assertIsNone(self.scene.config_dict)
	
	def test_Scene_ParsesYamlConfig(self):
		expected_value = config_string
		self.scene.parse_yaml_config(config_string)
		self.assertTrue(self.scene.config_dict == yaml.load(config_string))

	def test_Scene_LoadsConfig_FromFile(self):
		tmp_config_file = tempfile.NamedTemporaryFile()
		tmp_config_file_path = tmp_config_file.name
		tmp_config_file.write(config_string)
		tmp_config_file.seek(0)

		scene = self.scene
	        scene.config_filepath = tmp_config_file_path
		self.assertIsNone(scene.config_dict)

		scene.load_config_from_file()
		self.assertEqual(scene.config_dict, yaml.load(config_string))
		
		tmp_config_file.close()

	def test_SatScene_PopulatesFromConfig(self):
		scene = self.scene
		scene.config_filepath = os.path.join('test_data', 'test_config.yml')
		scene.input_filename = self.input_filename
		scene.load_config_from_file()
		scene.get_bands()
		self.assertTrue(hasattr(scene, scene.config_dict.keys()[0]))

	def test_SatScene_ObtainsCoordinates(self):
		scene = data.SwathScene()
		scene.config_filepath = os.path.join('test_data', 'test_config.yml')
		scene.input_filename = self.input_filename
		scene.load_config_from_file()
		scene.get_coordinates()
		scene.get_bands()
		self.assertIsNotNone(scene.latitudes)
		self.assertIsNotNone(scene.longitudes)
		self.assertIsNotNone(scene.bands)
