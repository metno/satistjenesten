import os
from satistjenesten import data
import netCDF4 as nc
import numpy

@given(u'we process file {netcdf_filepath}')
def step_impl(context, netcdf_filepath):
	context.netcdf_filepath = netcdf_filepath

@then(u'load the file using yaml config {avhrr_l1b_yaml_config}')
def step_impl(context, avhrr_l1b_yaml_config):
	context.config_filepath = avhrr_l1b_yaml_config
	scene = data.SatScene()
	scene.config_filepath = context.config_filepath
	scene.input_filename = context.netcdf_filepath
	scene.load_scene_from_disk()
	expected_variable = nc.Dataset(context.netcdf_filepath).variables['reflec_1'][:]
	numpy.testing.assert_array_almost_equal(scene.bands['reflec_1'].data,expected_variable)
	

@then(u'resample it to the istjenesten generic area {area_name}')
def step_impl(context, area_name):
	context.avhrr_scene.area_name = area_name
	context.avhrr_scene.resample()
	assert False

@then(u'export it as a netcdf file {output_file}')
def step_impl(context, output_file):
	context.output_file = output_file
	context.avhrr_scene.write_as_netcdf(output_file)
	assert False
