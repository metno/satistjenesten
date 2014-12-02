Feature: compute sea ice concentration
    As a developer of MAD
    When processing AVHRR L1B files
    I want to compute SIC using various algorithms

    Background:
        Given using <config_filepath>

    Scenario Outline: Dummy SIC
        When processing <input_file>
        And using <sic_algorithm>
        Then get file with sic
        And with mean sic value <value>

        Examples: LAC data
            | input_file | sic_algorithm | value | config_file |
            | test_data/metop-b.nc | dummy_sic | 1 | files/avhrr_beam.yml |
