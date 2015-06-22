#!/bin/bash
set -e
export PYTHONPATH=/disk1/workspace/satistjenesten
TIMESPAN=550
FILES=$(find /opdata/satdata_polar/viirs-ears/mitiff/ -name viirs-ears-20*.mitiff -cmin -$TIMESPAN)
CHANNELS="4 3 2"
AREA="istjenesten_main_500m"
SAT="viirs-ears"
OUTDIR=$HOME/mnt/is_data/VIIRS/GeoTIFF
if [ ! -d "$OUTDIR" ]; then
    echo "$OUTDIR" does not exist
    exit 1
fi
/usr/bin/env python ./mitiff_mosaic.py  -s $SAT   \
                                                -i $FILES \
                                                -c $CHANNELS \
                                                -a $AREA \
                                                -o $OUTDIR

