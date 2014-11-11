#!/usr/bin/env python

import os

def get_project_root_path():
    try:
        project_path = os.environ['ICE_HOME']
    except:
        project_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    return project_path

def get_area_filepath():
    project_path = get_project_root_path()
    area_filepath = os.path.join(project_path, 'areas.cfg')
    return area_filepath
