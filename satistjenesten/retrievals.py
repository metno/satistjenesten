#!/usr/bin/env python

from satistjenesten import data
import numpy

def compute_parameter(scene, alg='dummy_sic'):
     eval("compute_{0}(scene)".format(alg))

def compute_dummy_sic(scene):
    """
    Compute sea ice concentration using a selection of algorithms
    Appends a new band with computed parameter

    Args:
        scene (data.SatScene): existing scene instance with loaded bands
        algorithm (string): name of the algorithm to use

    """
    reflec_1 = scene.bands['reflec_1'].data
    sic_array = numpy.ones(reflec_1.shape)
    sic_band = data.SatBand()
    sic_band.data = sic_array
    sic_band.long_name = 'Dummy SIC'
    scene.bands['sic'] = sic_band
