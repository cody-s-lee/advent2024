import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs="*", help="Days to run")
    parser.add_argument("-x", "--example", action="store_true", help="Use example file")
    parser.add_argument("-a", "--all", action="store_true", help="Run all days")
    return parser.parse_args()


def with_lines(func):
    def wrapper(contents):
        return func(contents.split("\n"))

    return wrapper


def with_content(func):
    def wrapper(contents):
        return func(contents)

    return wrapper
