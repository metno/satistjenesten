from pycoast import ContourWriter
from PIL import ImageFont

def add_graticules_to_img(scene):
	font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf",16)
	cw = ContourWriter('/disk1/workspace/gshhs')
	area_def = (scene.area_def.proj_dict, scene.area_def.area_extent )
	cw.add_coastlines(scene.img, area_def, resolution = 'h', outline='yellow')
	cw.add_grid(scene.img, area_def, (1, 1), (0.5, 0.5), font,
            outline='blue', write_text = True, minor_outline=(255, 0, 0))
	scene.img.save('/tmp/modis-barent.png')