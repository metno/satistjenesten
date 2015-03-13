from satistjenesten import GenericScene

class MosaicScene(GenericScene):
    """
    Mosaic scene is an extension of GenericScene where
    Several scenes are combined into one
    """
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None
        self.timestamp = None
        self.area_def = None

    def add_scenes(self, scenes_list):
        background_scene = self.scenes_list[0]
        if self.area_def is None:
            self.area_def = background_scene.area_def
            self.start_timestamp = background_scene.timestamp
        self.scenes = scenes_list
