import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("-x", "--example", action="store_true", help="Use example file")
    parser.add_argument("-a", "--answers", type=int, nargs='*', help="Answers to the parts")
    return parser.parse_args()