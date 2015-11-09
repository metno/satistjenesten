Feature: As a user of the software
	I want to be able to read and write satellite data in various formats

	Scenario Outline: Read and Write
		Given we process mitiff file <input_filepath>
		Then export a geotiff file <output_file>

		Examples:
			| input_filepath | yaml_config | area_name | output_file |
			| test_data/avhrr-swath.mitiff | None | nsidc_stere_north_300k | out.tif |

    @wip
    Scenario Outline: Read and Write Netcdf Files
        Given we process netcdf file <input_filepath>
        Then resample to the <area_name>
        Then export a geotiff file <output_file>

        Examples:
            | input_filepath | area_name | output_file |
            | test_data/amsr2.nc | istjenesten_frode | amsr2.tif |

    @wip
    Scenario Outline: Read GeoTIFF files
        Given we process GeoTIFF file <input_filepath>
        Then export a geotiff file <output_file>
        Then export an image <image_file> with graphics

        Examples:
            | input_filepath | area_name | output_file | image_file |
            | test_data/modis.tif |  nsidc_stere_north_300k | modis-output.tif | coastlines.png |
