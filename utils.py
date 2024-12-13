import argparse
import typing


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


class Point(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def mul_scalar(self, scalar):
        return Point(self.x * scalar, self.y * scalar)


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
CARDINAL_DIRECTIONS = [N, E, S, W]


def add_points(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)


def neighbors(p: Point) -> list[Point]:
    return [Point(p.x + 1, p.y), Point(p.x - 1, p.y), Point(p.x, p.y + 1), Point(p.x, p.y - 1)]


def one_of(s: set):
    e = None
    for e in s:
        break
    return e
