import os
from pycoast import ContourWriter
from PIL import ImageFont

image_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), os.pardir,
                        'test_data', 'DejaVuSerif.ttf'), 16)
gshhs_dir =  os.path.join(os.path.dirname(__file__), os.pardir, 'test_data', 'gshhs')

def add_graticules_to_img(scene):
	font = image_font
	cw = ContourWriter(gshhs_dir)

	area_def = (scene.area_def.proj_dict, scene.area_def.area_extent )

	cw.add_coastlines(scene.img, area_def, resolution = 'l', level=4, outline='yellow')
	cw.add_grid(scene.img, area_def, (1, 1), (0.5, 0.5), font,
            outline='blue', write_text = True, minor_outline=(255, 0, 0))
	scene.img.save('/tmp/modis-barent.png')
