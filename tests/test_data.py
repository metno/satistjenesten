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




class TestSceneResampling(unittest.TestCase):
    def setUp(self):
            self.scene = data.SatScene()
            self.scene.file_path = os.path.join('test_data', 'avhrr-msv.mitiff')
            self.scene.config_path = os.path.join('test_data', 'avhrr-mitiff.yml')
            self.scene.load()

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
