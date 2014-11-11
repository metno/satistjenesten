Feature: As a user of the software
	I want to read satellite data
	Then I want to resample all the channels inside
 	Then I want to save the results in netcdf format

	Scenario Outline: Beam Avhrr Netcdf files
		Given we process file <netcdf_filepath>
		Then load the file using yaml config <avhrr_l1b_yaml_config>
		Then resample it to the istjenesten generic area <area_name>
		Then export it as a netcdf file <output_file>

		Examples:
			| netcdf_filepath | avhrr_l1b_yaml_config | area_name | output_file |
			| test_data/metop-b.nc | test_data/test_config.yml | nsidc_stere_north_300k | resampled_avhrrl1b.nc |


