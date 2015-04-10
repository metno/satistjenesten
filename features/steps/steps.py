import os
import netCDF4 as nc
import numpy
import pyresample

from satistjenesten import io


@given(u'we process mitiff file {input_filepath}')
def step_impl(context, input_filepath):
    context.input_filepath = input_filepath
    context.scene = io.load_mitiff(input_filepath)
    assert context.scene.area_def is not None

@then(u'export a geotiff file {output_filepath}')
def step_impl(context, output_filepath):
    context.scene.save_geotiff(output_filepath, cmap='istjenesten')

@given(u'we process netcdf file {input_filepath}')
def step_impl(context, input_filepath):
    context.scene = io.load_netcdf(input_filepath, bands = ['ct_n90_OSISAF_corrNASA_wWF'])

@then(u'resample to {area_name}')
def step_impl(context, area_name):
    area = pyresample.utils.load_area('areas.cfg', 'istjenesten_main_4k')
    context.scene = context.scene.resample_to_area(area)
