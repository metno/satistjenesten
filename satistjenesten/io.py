import yaml
import collections
import numpy

from PIL import Image
from satistjenesten.data import SatBand

class Mitiff(object):
    def __init__(self):
        self.filename = None
        self.bands = None
        self.longitudes = None
        self.latitudes = None
        self.yaml_dict = None
    
    def load(self):
        self.get_image()
        self.get_mitiff_bands()

    def get_image(self):
        self.image = Image.open(self.filename)
    
    def get_mitiff_bands(self):
        bands = collections.OrderedDict()
        yaml_dict = load_yaml_config(self.yaml_dict)
        band_dict = yaml_dict['bands']
        for (band_name, band_value) in band_dict.items():
            sat_band = SatBand()
            band_id = int(band_name)
            self.image.seek(band_id)
            sat_band.data = numpy.array(self.image)
            sat_band.long_name = band_value['long_name']
            bands[band_name] = sat_band
        self.bands = bands

def load_yaml_config(filepath):
    with open(filepath, 'r') as fh:
        yaml_dict = yaml.load(fh)
    return yaml_dict

