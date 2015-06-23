import unittest
import pyresample
import satistjenesten
import rasterio


class TestUtils(unittest.TestCase):
	def setUp(self):
		self.gtiff_fh = rasterio.open('test_data/modis.tif')

	def test_geotiff_to_areadef(self):
		gtiff_meta_dict = self.gtiff_fh.meta
		area_def = satistjenesten.utils.geotiff_meta_to_areadef(gtiff_meta_dict)
		self.assertIsInstance(area_def, pyresample.geometry.AreaDefinition)