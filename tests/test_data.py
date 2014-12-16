import unittest
import tempfile
import yaml
import os
import numpy
import netCDF4

from satistjenesten import data

config_string = """
bands:
  reflec_1:
    long_name: reflectivity
latitude_name: latitude
longitude_name: longitude
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
            scene = data.SwathSatScene()
            scene.config_filepath = os.path.join('test_data', 'test_config.yml')
            scene.input_filename = self.input_filename
            scene.load_config_from_file()
            scene.get_coordinates()
            self.assertIsNotNone(scene.latitudes)
            self.assertIsNotNone(scene.longitudes)


class TestSceneResampling(unittest.TestCase):
    def setUp(self):
            self.scene = data.SatScene()
            self.scene.input_filename = os.path.join('test_data', 'metop-b.nc')
            self.scene.config_filepath = os.path.join('test_data', 'test_config.yml')
            self.scene.load_scene_from_disk()

    def test_SatScene_ResamplesToDefinedArea(self):
            scene = self.scene
            scene.area_name = 'nsidc_stere_north_300k'
            gridded_scene = scene.resample_to_area()
            self.assertTrue(gridded_scene.area_def is not None)
            self.assertTrue(gridded_scene.gridded)


class TestExportNetcdf(unittest.TestCase):
        def setUp(self):
            self.output_filepath = "/tmp/t.nc"
            self.scene = data.GriddedSatScene()
            self.scene.bands['test_band'] = data.SatBand()
            self.array_shape = (100, 100)
            self.scene.bands['test_band'].data = numpy.random.rand(100, 100)

        def test_Save_SatScene_AsNetcdf(self):
            scene = self.scene
            scene.output_filepath = self.output_filepath
            scene.write_as_netcdf()
            output_dataset = netCDF4.Dataset(self.output_filepath, 'r')
            self.assertTrue(isinstance(output_dataset, netCDF4.Dataset))

        def tearDown(self):
            # os.remove(self.output_filepath)
            pass

class TestRescale(unittest.TestCase):
    def setUp(self):
        self.array = numpy.ones((10, 10))

    def test_window_blocks_Returns_Smaller_Array(self):
        large_array = self.array
        flat_large_array = large_array.flatten()
        window_size = 4
        expected_number_of_blocks = flat_large_array.shape[0] / window_size
        small_array = data.window_blocks(flat_large_array, 4)
        self.assertSequenceEqual((expected_number_of_blocks, window_size), small_array.shape)
