#!/bin/bash
# Mikhail Itkin, Norwegian Ice Service
#
# Script that finds satellite imagery files
# which are less that $TIMESPAN minutes old
# and produces a mosaic for a combination of $CHANNELS
#
# Last modification date:
#   Thu Mar 26 12:15:44 CET 2015

set -e

function generate_mosaic() {

# the is used as follows:
# generate_mosaic SENSOR_NAME 
#		  TIME_INTERVAL - search for files younger then age in minutes 		  
#		  INPUT_DIRECTORY 
#		  VARIABLE_NAME - which band (or bands) to process
# 		  AREA_NAME - Area defintion ID
# 		  OUTPUT_DIRECTORY

SAT=$1
TIMESPAN=$2
INDIR=$3
FILES=$(find "$INDIR" -cmin -$TIMESPAN -type f)
CHANNELS=$4
AREA=$5
OUTDIR=$6


if [ ! -d "$OUTDIR" ]; then
    echo "$OUTDIR" does not exist
    exit 1
fi

export PYTHONPATH=$HOME/satistjenesten
export BINDIR=$PYTHONPATH
/usr/bin/env python "$BINDIR"/scripts/amsr2_mosaic.py  -s $SAT   \
                                                -i $FILES \
                                                -b $CHANNELS \
                                                -a $AREA \
                                                -o $OUTDIR
}


generate_mosaic "ASMR2" \
		"720" \
		"/vol/fou/sat/atlems/amsr" \
		"ct_n90_OSISAF_corrNASA_wWF" \
		"istjenesten_stere_north_3k" \
		./
