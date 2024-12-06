import argparse
from collections import namedtuple


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs="*", help="Days to run")
    parser.add_argument("-x", "--example", action="store_true", help="Use example file")
    parser.add_argument("-a", "--all", action="store_true", help="Run all days")
    return parser.parse_args()


def with_lines(func):
    def wrapper(contents):
        return func(contents.rstrip(' \n').split("\n"))

    return wrapper


def with_content(func):
    def wrapper(contents):
        return func(contents.rstrip(' \n'))

    return wrapper


Point = namedtuple('Point', ['x', 'y'])


def add_points(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)
