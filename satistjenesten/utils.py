import os
import yaml
import pyresample

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

def load_area_def(area_name):
    path_to_area_cfg = get_area_filepath()
    area_def = pyresample.utils.load_area(path_to_area_cfg, area_name)
    return area_def

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

def window_blocks(large_array, window_size):
    """
    Split a large 1D array into smaller non-overlapping arrays

    Args:
      large_array (numpy.ndarray): 1d array to be split in smaller blocks
      window_size (int): window size, array shape should be divisible by this number

    Returns:
     numpy.ndarray: Resulting array with multiple small blocks of size `window_size`

    """
    y_size = large_array.shape[0]/window_size
    blocks_array = large_array.reshape(y_size, window_size)
    return blocks_array

def rescale_lac_array_to_gac(lac_array):
    """
    Create a GAC AVHRR array by averaging 4 consecutive LAC pixels
    Take only every forth scan line, omit the rest

    Args:
      lac_array (numpy.ndtype): array with scan width of 2001 pixels

    Returns:
      gac_array (numpy.ndtype): array with scan width of 400 pixels

    Note:
      Original GAC data contains 401 pixels per scanline, for the sake
      of simplicity we take only 400 pixels.

    """
    window_size = 5
    lac_array_with_omitted_lines = lac_array[::4]
    lac_array_2000px = lac_array_with_omitted_lines[:,:-1]
    flat_lac_array = lac_array_2000px.flatten()
    gac_array_flat = np.mean(window_blocks(flat_lac_array, window_size)[:,:-1], axis=1)
    gac_length = gac_array_flat.shape[0]
    gac_array_2d = gac_array_flat.reshape(gac_length/400, 400)
    return gac_array_2d

def parse_proj_string(proj_string):
    """
    Parse proj4 string and create a dictionary out of it
    """
    regex_pattern = "(\+(\w+)=([A-Z\d+\w+\.]*))"
    regex = re.compile(regex_pattern)
    regex_results = regex.findall(proj_string)
    proj_dict = {}
    for proj_element in regex_results:
        proj_dict[proj_element[1]] = proj_element[2]
    return proj_dict
