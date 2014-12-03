@wip
Feature: compute sea ice concentration
    As a developer of MAD
    When processing AVHRR L1B files
    I want to compute SIC using various algorithms

    Background:
        Given using AVHRR L1B Beam config

    Scenario Outline: Dummy SIC
        When processing <input_file> file
        And computing sic using <sic_algorithm> algorithm
        Then get file with sic data
        And with mean sic value <value>

        Examples: LAC data
            | input_file | sic_algorithm | value |
            | test_data/metop-b.nc | dummy_sic | 1 |
