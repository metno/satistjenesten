import unittest
from satistjenesten import io
import numpy
import datetime

class TestIoMitiff(unittest.TestCase):

    def setUp(self):
        mitiff_file_path = 'test_data/avhrr-swath.mitiff'
        mitiff = io.MitiffScene(filepath=mitiff_file_path)
        mitiff.load()
        self.mitiff = mitiff

    def tearDown(self):
        del self.mitiff

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


    def test_get_timestamp(self):
        self.mitiff.get_mitiff_tags()
        self.mitiff.get_timestamp()
        self.assertIsInstance(self.mitiff.timestamp, datetime.datetime)

class TestIoNetcdf(unittest.TestCase):
    def setUp(self):
        netcdf_filepath = 'test_data/amsr2.nc'
        netcdf_scene = io.NetcdfScene(filepath=netcdf_filepath, bands=['lat_h'])
        self.netcdf = netcdf_scene
        self.netcdf.load()

    def test_Load_DefinedBands(self):
        self.assertIsNotNone(self.netcdf.bands)
