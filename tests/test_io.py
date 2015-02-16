import unittest
from satistjenesten import io
import numpy

class TestIoMitiff(unittest.TestCase):
    
    def setUp(self):
        mitiff_file_path = 'test_data/avhrr-msv.mitiff'
        mitiff_dict_path = 'test_data/avhrr-mitiff.yml'
        mitiff = io.Mitiff()
        mitiff.filename = mitiff_file_path
        mitiff.yaml_dict = mitiff_dict_path
        self.mitiff = mitiff

    def test_load_NumpyArray(self):
        self.mitiff.load()
        bands = self.mitiff.bands
        numpy_band = bands.values()[0].data
        self.assertIsInstance(numpy_band, numpy.ndarray)

    def test_parse_MitiffHeader(self):
        pass

    def test_construct_coordinate_arrays(self):
        pass

    def test_get_timestamp(self):
        pass
