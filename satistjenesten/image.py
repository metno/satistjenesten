import os
from pycoast import ContourWriterAGG
from PIL import ImageFont, ImageDraw, Image, ImageFile
import aggdraw

font_filepath = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font = aggdraw.Font('blue', font_filepath, size=56, opacity=200)
pil_font = ImageFont.truetype(font_filepath, 90)
gshhs_dir =  os.path.join(os.path.dirname(__file__), os.pardir, 'test_data', 'gshhs')
gshhs_dir =  '/disk1/mikhaili/gshhs'

def add_graticules_to_img(scene):
    cw = ContourWriterAGG(gshhs_dir)

    area_def = (scene.area_def.proj_dict, scene.area_def.area_extent )
    area_def = scene.area_def
    area_def.proj4_string.encode('ascii')
    # cw.add_overlay_from_config('config/pycoast.config', area_def)


    cw.add_coastlines(scene.img, area_def,
                            resolution = 'h',
                            level=4,
                            outline='yellow',
                            width=5)

    cw.add_grid(scene.img, area_def, (5, 5), (2.5, 2.5), font, width=1.4,
            outline='blue', write_text = True, minor_outline='blue')

def add_caption_to_img(scene, text):
    """
    Add a white box on top of the image and paste some text there
    """

    image = scene.img

    W, H = image.size
    dy = int(H * 0.05)
    print image.size

    # add box on top
    larger_image = Image.new('RGB', (W, H + dy), color='white')
    larger_image.paste(image, (0, dy))

    # add text
    draw = ImageDraw.Draw(larger_image)
    caption_font = pil_font
    text_width, text_height = draw.textsize(text, font = pil_font)

    draw.text(((W - text_width)/2, (dy - text_height)/2), 
                                                        text=text,
                                                        fill='black',
                                                        font=caption_font)

    scene.img = larger_image

def save_reduced_jpeg( scene, jpeg_fname, target_size):
    """
    Rescale scene.image and save as JPEG not larger than target_size

    Parameters:
    scene (GenericScene): input scene with 'img' attribute
    jpeg_fname (str): output filename of JPEG file
    target_size (float): the targe size of the output JPEG file
 
    """
    ImageFile.MAXBLOCK = 2**30

    im = scene.img
    size = im.size
    # Reduce size of image
    fraction = 2
    width = size[0] / fraction
    height = size[1] / fraction
    im = im.resize( (width,height), Image.ANTIALIAS )

    # Loop through, reducing quality until we obtain target size
    quality = 95
    im.save( jpeg_fname, "JPEG", quality=quality, optimize=True, progressive=True )
    jpegsize = float( (os.stat( jpeg_fname )).st_size ) / 1024.0

    while jpegsize > target_size and quality > 25:
        quality = quality - 5
        im.save( jpeg_fname, "JPEG", quality=quality, optimize=True, progressive=True )
        jpegsize = float( (os.stat( jpeg_fname )).st_size ) / 1024.0
