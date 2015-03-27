from satistjenesten import GenericScene

class ImageScene(GenericScene):
    def __init__(self):
        self.bands = None

    def create_rgb(self, red_band, green_band, blue_band):
        red = red_band.data
        gree = green_band.data
        blue = blue_band.data
        self.bands['rgb'] = numpy.dstack((red, green, blue))

