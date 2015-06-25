import os
from pycoast import ContourWriterAGG
from PIL import ImageFont
import aggdraw
font = aggdraw.Font('blue', os.path.join(os.path.dirname(__file__), os.pardir, 'test_data', 'DejaVuSerif.ttf'), size=16, opacity=200)
gshhs_dir =  os.path.join(os.path.dirname(__file__), os.pardir, 'test_data', 'gshhs')

def add_graticules_to_img(scene):
	cw = ContourWriterAGG(gshhs_dir)
	area_def = (scene.area_def.proj_dict, scene.area_def.area_extent )
        area_def = scene.area_def
        area_def.proj4_string.encode('ascii')
        # cw.add_overlay_from_config('config/pycoast.config', area_def)


	cw.add_coastlines(scene.img, area_def, resolution = 'l', level=4, outline='yellow',width=2)
	cw.add_grid(scene.img, area_def, (1, 1), (0.5, 0.5), font, width=3,
            outline='blue', write_text = True, minor_outline=(255, 0, 0))
