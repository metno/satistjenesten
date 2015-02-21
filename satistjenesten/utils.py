import os
import yaml

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

def parse_extension(filepath):
    """
    Parse file extension and return format string
    to make other bits aware which format driver should be used
    """
    extension = os.path.splitext(filepath)[1][1:]

    extensions_dict = {"netcdf": ['nc'],
                       "mitiff": ['mitiff'],
                       "geotiff": ['gtiff', 'tiff', 'tif']}

    driver = None

    for key in extensions_dict:
        if extension in extensions_dict[key]:
           driver = key 

    if driver is not None:
        return driver
    else:
        raise Exception("Unknown file extension, cannot guess file format")

def load_yaml_config(filepath):
    with open(filepath, 'r') as fh:
        yaml_dict = yaml.load(fh)
    return yaml_dict

