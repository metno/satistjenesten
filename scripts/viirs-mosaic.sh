#!/bin/bash
set -e
export PYTHONPATH=/disk1/workspace/satistjenesten
TIMESPAN=550
FILES=$(find /opdata/satdata_polar/viirs-ears/mitiff/ -name viirs-ears-20*.mitiff -cmin -$TIMESPAN)
CHANNELS="4 3 2"
AREA="istjenesten_main_500m"
SAT="viirs-ears"
OUTDIR=.

/usr/bin/env python ./scripts/mitiff_mosaic.py  -s $SAT   \
                                                -i $FILES \
                                                -c $CHANNELS \
                                                -a $AREA \
                                                -o $OUTDIR
