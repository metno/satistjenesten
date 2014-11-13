import argparse
from satistjenesten import data

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filepath', nargs=1, type=str)
    parser.add_argument('output_filepath', nargs=1)
    parser.add_argument('--config_filepath', '-c', required=True)
    parser.add_argument('--area_name', '-a', default='nsidc_stere_north_300k')
    args = parser.parse_args()
    return args

def __main__():

    args = parse_args()
    scene = data.SatScene()
    scene.config_filepath = args.config_filepath
    scene.input_filename = args.input_filepath[0]
    scene.load_scene_from_disk()
    scene.area_name = args.area_name

    gridded_scene = scene.resample_to_area()
    gridded_scene.output_filepath = args.output_filepath[0]
    gridded_scene.write_as_netcdf()


if __name__ == "__main__":
    __main__()
