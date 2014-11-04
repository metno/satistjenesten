import os
import satistjenesten

@given(u'we process file {netcdf_filepath}')
def step_impl(context, netcdf_filepath):
	context.netcdf_filepath = netcdf_filepath

@then(u'load the file using yaml config {avhrr_l1b_yaml_config}')
def step_impl(context, avhrr_l1b_yaml_config):
	context.avhrr_l1b_yaml_config = avhrr_l1b_yaml_config
	context.avhrr_scene = satistjenesten.data.SatScene()
	context.avhrr_scene.config_file = avhrr_l1b_yaml_config
	context.avhrr_scene.load()
	assert False

@then(u'resample it to the istjenesten generic area {area_name}')
def step_impl(context, area_name):
	context.avhrr_scene.area_name = area_name
	context.avhrr_scene.resample()
	assert False

@then(u'export it as a netcdf file {output_file}')
def step_impl(context, output_file):
	context.output_file = output_file
	context.avhrr_scene.write_netcdf(output_file)
	assert False
