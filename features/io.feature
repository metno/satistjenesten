Feature: As a user of the software
	I want to be able to read and write satellite data in various formats

    @wip
	Scenario Outline: Read and Write
		Given we process file <input_filepath>
		Then load the file using yaml config <yaml_config>
		Then export it as a file <output_file>

		Examples:
			| input_filepath | yaml_config | area_name | output_file |
			| test_data/metop-b.nc | test_data/test_config.yml | nsidc_stere_north_300k | resampled_avhrrl1b.nc |
			| test_data/avhrr-msv.mitiff | test_data/avhrr-mitiff.yml | nsidc_stere_north_300k | resampled_avhrrl1b.nc |
