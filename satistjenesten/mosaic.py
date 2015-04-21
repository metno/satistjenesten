from satistjenesten.scene import GenericScene
import numpy

class MosaicScene(GenericScene):
    """
    Mosaic scene is an extension of GenericScene where
    Several scenes are combined into one
    """

    def compose_mosaic(self, scenes_list, resample_method='nn'):

        self.scenes = sort_scenes_by_timestamp(scenes_list)
        background_scene = self.scenes[0]

        # Start with second scene in the list, as the first one
        # has been added already as a background scene
        scene_list = self.scenes

        for scene in scene_list:
            if scene.area_def != self.area_def:
                resampled_scene = scene.resample_to_area(self.area_def,
                                               resample_method=resample_method)

            self.overlay_mosaic_bands(resampled_scene)

        self.start_timestamp = self.scenes[0].timestamp
        self.end_timestamp = self.scenes[-1].timestamp
        self.end_timestamp_string = self.end_timestamp.strftime('%Y%m%d%H%M')
        self.start_timestamp_string = self.start_timestamp.strftime('%Y%m%d%H%M')

    def overlay_mosaic_bands(self, scene):

        if self.bands is None:
            self.bands = scene.bands

        for band_name in self.bands.keys():
            mosaic_band = self.bands[band_name].data.copy()
            scene_band = scene.bands[band_name].data.copy()
            # XXX: Using zeroes instead of fill_values. Not good!
            # TODO: Handle missing data correctly
            self.bands[band_name].data = numpy.where(scene_band == 0,
                    mosaic_band,
                    scene_band)

def sort_scenes_by_timestamp(scenes_list):
    """
    Sort list of scenes using timestamp

    """
    sorted_list = sorted(scenes_list, key=lambda scene: scene.timestamp)
    return sorted_list
