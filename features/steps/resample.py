import os

@given(u'we process file {netcdf_filepath}')
def step_impl(context, netcdf_filepath):
	context.netcdf_filepath = netcdf_filepath
	assert True

@then(u'load the file using yaml config {avhrr_l1b_yaml_config}')
def step_impl(context, avhrr_l1b_yaml_config):
	context.avhrr_l1b_yaml_config = avhrr_l1b_yaml_config
	assert True

@then(u'resample it to the istjenesten generic area {area_name}')
def step_impl(context, area_name):
	context.area_name = area_name
	assert True

@then(u'export it as a netcdf file {output_file}')
def step_impl(context, output_file):
	context.output_file = output_file
	assert True
