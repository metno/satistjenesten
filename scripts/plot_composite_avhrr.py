#!/usr/bin/env python
import sys
from PIL import Image, ImageOps
from matplotlib.pyplot import imshow, savefig, title
import netCDF4 as nc
import numpy as np
ifile = sys.argv[1]
ofile = "{0}.png".format(ifile)
nc_dataset = nc.Dataset(ifile, 'r')
r = nc_dataset.variables['reflec_1'][:]
g = nc_dataset.variables['reflec_2'][:]
b = nc_dataset.variables['temp_4'][:]
b_norm = (b - b.min()) / (b.max() - b.min()) * 100
rgb = np.dstack((r, g, b_norm)) / 100.
rgb_uint8 = (rgb * 255.999).astype(np.uint8)
img = Image.fromarray(rgb_uint8)
img_eq = ImageOps.equalize(img)

# title(ifile)
# savefig(ofile)
img_eq.save(ofile)
