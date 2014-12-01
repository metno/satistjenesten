from satistjenesten import data
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs=1)
    parser.add_argument('output_file', nargs=1)
    parser.add_argument('-c', '--config_file')
    args = parser.parse_args()
    return args


def __main__():
    args = parse_args()
    input_file = args.input_file[0]
    output_file = args.output_file[0]
    scene = data.SatScene()
    scene.config_filepath = args.config_file
    scene.input_filename = input_file
    scene.output_filepath = output_file
    scene.load_scene_from_disk()
    scene.resample_to_gac()
    scene.write_as_netcdf()

if __name__ == "__main__":
    __main__()
