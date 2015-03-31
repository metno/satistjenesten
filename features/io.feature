Feature: As a user of the software
	I want to be able to read and write satellite data in various formats

	Scenario Outline: Read and Write
		Given we process mitiff file <input_filepath>
		Then export a geotiff file <output_file>

		Examples:
			| input_filepath | yaml_config | area_name | output_file |
			| test_data/avhrr-msv.mitiff | None | nsidc_stere_north_300k | out.tif |

    @wip
    Scenario Outline: Read and Write Netcdf Files
        Given we process netcdf file <input_filepath>
        Then resample to the <area_name>
        Then export a geotiff file <output_file>

        Examples:
            | input_filepath | area_name | output_file |
            | test_data/amsr2n90.nc | istjenesten_main_4k | amsr2.tif |
