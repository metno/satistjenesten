import unittest
from satistjenesten.scene import GenericScene
from satistjenesten.scene import SatBand
import pyresample as pr
import numpy

class TestScene(unittest.TestCase):
    def setUp(self):
        area_name = 'nsidc_stere_north_300k'
        area_def = pr.utils.load_area('./areas.cfg', area_name)
        self.area_def = area_def
        self.scene = GenericScene()
        self.scene.get_area_def(area_name)
        band = SatBand()
        band.data = numpy.ones((self.area_def.x_size, self.area_def.y_size))
        self.scene.bands = {'1': band}

    def test_Scene_ResampleToArea_withGaussianResampling(self):
        res = self.scene.resample_to_area(self.area_def, resample_method='gaussian')

    def test_Scene_ResampleToArea_withNearestNeighbourResampling(self):
        res = self.scene.resample_to_area(self.area_def, resample_method='nn')

    def test_Scene_ResampleToArea_InvalidResampleMethod_RaisesException(self):
        with self.assertRaises(Exception):
            self.scene.resample_to_area(self.area_def, resample_method='foo')

