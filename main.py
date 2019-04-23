import argparse

import utils


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infolder", nargs="?", type=str)
    parser.add_argument("--pattern", nargs="?", type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_commandline_arguments()

    if args.infolder:
        if args.pattern:
            utils.generate_behavioral_dataset(args.infolder, args.pattern)
        else:
            raise Exception("Need to inform the file pattern!")
    else:
        raise Exception("Need to inform the input folder!")
