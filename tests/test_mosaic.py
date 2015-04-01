import unittest
import os
from satistjenesten.mosaic import MosaicScene
from satistjenesten.io import load_osisaf_amsr2_netcdf

class TestMosaicScene(unittest.TestCase):
    def setUp(self):
        self.bands_list = ['lat_h']
        self.scene_1 = load_osisaf_amsr2_netcdf('test_data/amsr2.nc', bands=self.bands_list)
        self.scene_2 = load_osisaf_amsr2_netcdf('test_data/amsr2.nc', bands=self.bands_list)
        self.mosaic = MosaicScene()
        self.mosaic.get_area_def(area_name='nsidc_stere_north_300k')

    def test_MosaicScene_AddsScenes(self):
        self.mosaic.add_scenes([self.scene_1])
        self.assertEquals(self.mosaic.start_timestamp, self.scene_1.timestamp)
        self.assertNotEquals(self.mosaic.area_def, self.scene_1.area_def)

    def test_MosaicScene_ComposeMosaic(self):
        self.mosaic.add_scenes([self.scene_1, self.scene_2])
        self.mosaic.compose_mosaic()
        self.mosaic.save_geotiff('out.tif', bands=self.bands_list)
        self.assertTrue(os.path.exists('out.tif'))
