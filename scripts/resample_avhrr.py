import argparse
from satistjenesten import data

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='*')
    args = parser.parse_args()
    return args

def __main__():
    args = parse_args()
    input_file = args.input
    print input_file

if __name__ == "__main__":
    __main__()
