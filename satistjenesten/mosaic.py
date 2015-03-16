from satistjenesten.scene import GenericScene
import numpy

class MosaicScene(GenericScene):
    """
    Mosaic scene is an extension of GenericScene where
    Several scenes are combined into one
    """

    def add_scenes(self, scenes_list):
        self.scenes = scenes_list
        background_scene = self.scenes[0]
        if self.area_def is None:
            self.area_def = background_scene.area_def
        if self.timestamp is None:
            self.start_timestamp = background_scene.timestamp
            self.timestamp = self.start_timestamp
        if self.area_def is not background_scene.area_def:
            self.bands = background_scene.resample_to_area(self.area_def).bands
        else:
            self.bands = background_scene.bands

    def compose_mosaic(self):
        if self.scenes is None:
            raise Warning("Can't compose mosaic before any scenes have been added")

        # Start with second scene in the list, as the first one
        # has been added already as a background scene
        scene_list = self.scenes[1:]
        for scene in scene_list:
            if scene.area_def != self.area_def:
                scene = scene.resample_to_area(self.area_def)
            self.add_bands_to_mosaic_bands(scene)
        # self.end_timestamp = scene_list[-1].timestamp 

    def add_bands_to_mosaic_bands(self, scene):
        for band_name in self.bands.keys():
            mosaic_band = self.bands[band_name].data.copy()
            scene_band = scene.bands[band_name].data.copy()
            # XXX: Using zeroes instead of fill_values. Not good!
            # TODO: Handle missing data correctly
            self.bands[band_name].data = numpy.where(scene_band == 0,
                    mosaic_band,
                    scene_band)
