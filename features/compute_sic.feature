Feature: compute sea ice concentration
    As a developer of MAD
    When processing AVHRR L1B files
    I want to compute SIC using various algorithms

    Background:
        Given using AVHRR L1B Beam config

    Scenario Outline: Dummy SIC
        When processing <input_file> file
        And computing sic using <sic_algorithm> algorithm
        Then resample scene to the area <area_name>
        Then save netcdf file <output_file>

        Examples: LAC data
            | input_file | sic_algorithm |  output_file | area_name |
            | test_data/metop-b.nc | dummy_sic | dummy_sic.nc | nsidc_stere_north_300k |
