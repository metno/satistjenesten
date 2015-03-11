import os
import netCDF4 as nc
import numpy
import pyresample

from satistjenesten import io


@given(u'we process mitiff file {input_filepath}')
def step_impl(context, input_filepath):
    context.input_filepath = input_filepath
    context.mitiff = io.load_mitiff(input_filepath)
    assert context.mitiff.area_def is not None

@then(u'export a geotiff file {output_filepath}')
def step_impl(context, output_filepath):
    context.mitiff.save_geotiff(output_filepath)
