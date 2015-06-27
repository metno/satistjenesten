#!/bin/bash
set -e

# activate virtual environment
VENV_DIR=/disk1/mikhaili/isvenv
. ${VENV_DIR}/bin/activate
SCRIPTS_DIR=/disk1/mikhaili/scripts

# test python is able to import satistjenesten
python -c 'import satistjenesten'

# find recent MODIS images for Poseidon
DATA_DIR=~/mnt/is_data/MODIS/Arctic/GeoTIFF
INPUT_FILES=`find ${DATA_DIR} -type f -name "*poseidon_*ch*-*tif" -cmin -500`
EXPORT_DIR=/disk2/istjenesten_data/MODIS/Arctic/Images/Poseidon

# add graticules, captions and coastlines to the
# geotiff image and save it as a jpeg to the EXPORT_DIR
${SCRIPTS_DIR}/add_graphics_poseidon.py -i ${INPUT_FILES} -o ${EXPORT_DIR}
