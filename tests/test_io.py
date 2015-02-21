import unittest
from satistjenesten import io
import numpy

class TestIoMitiff(unittest.TestCase):

    def setUp(self):
        mitiff_file_path = 'test_data/avhrr-msv.mitiff'
        mitiff_dict_path = 'test_data/avhrr-mitiff.yml'
        mitiff = io.Mitiff(mitiff_file_path, mitiff_dict_path)
        self.mitiff = mitiff

    def test_load_NumpyArray(self):
        self.mitiff.load()
        bands = self.mitiff.bands
        numpy_band = bands.values()[0].data
        self.assertIsInstance(numpy_band, numpy.ndarray)

    def test_parse_MitiffTags(self):
        self.mitiff.load()
        self.mitiff.get_mitiff_tags()
        self.assertIsNotNone(self.mitiff.tags_dict['satellite'])
        self.assertIsNotNone(self.mitiff.tags_dict['timestamp'])
        self.assertIsNotNone(self.mitiff.tags_dict['x0'])
        self.assertIsNotNone(self.mitiff.tags_dict['y0'])
        self.assertIsNotNone(self.mitiff.tags_dict['xsize'])
        self.assertIsNotNone(self.mitiff.tags_dict['ysize'])
        self.assertIsNotNone(self.mitiff.tags_dict['x_px_size'])
        self.assertIsNotNone(self.mitiff.tags_dict['y_px_size'])

    def test_get_AreaDef_from_MitiffTags(self):
        self.mitiff.load()
        self.mitiff.get_mitiff_tags()
        self.mitiff.get_area_def()
        self.assertIsNotNone(self.mitiff.area_def)

    def test_construct_coordinate_arrays(self):
        pass

    def test_get_timestamp(self):
        pass
