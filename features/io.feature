Feature: As a user of the software
	I want to be able to read and write satellite data in various formats

    @wip
	Scenario Outline: Read and Write
		Given we process mitiff file <input_filepath>
		Then export a geotiff file <output_file>

		Examples:
			| input_filepath | yaml_config | area_name | output_file |
			| test_data/avhrr-msv.mitiff | None | nsidc_stere_north_300k | out.tif |
