import argparse
import typing
from enum import Enum


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs="*", help="Days to run")
    parser.add_argument("-x", "--example", action="store_true", help="Use example file")
    parser.add_argument("-a", "--all", action="store_true", help="Run all days")
    return parser.parse_args()


def is_example():
    return get_args().example


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

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def at_dist(self, dist):
        for x in range(-dist, dist + 1):
            y = dist - abs(x)
            yield Point(self.x + x, self.y + y)
            if y != 0:
                yield Point(self.x + x, self.y - y)


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
CARDINAL_DIRECTIONS = [N, E, S, W]
ORDINAL_DIRECTIONS = [N + E, S + E, S + W, N + W]
COMPASS_DIRECTIONS = CARDINAL_DIRECTIONS + ORDINAL_DIRECTIONS


class Direction(Enum):
    NORTH = N = N
    EAST = E = E
    SOUTH = S = S
    WEST = W = W


NEXT_DIRECTION = {
    N: E,
    E: S,
    S: W,
    W: N,
}

PREV_DIRECTION = {
    N: W,
    E: N,
    S: E,
    W: S,
}


def add_points(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)


def neighbors(p: Point, directions=None) -> list[Point]:
    if directions is None:
        directions = CARDINAL_DIRECTIONS
    return [p + d for d in directions]


def one_of(s: set):
    e = None
    for e in s:
        break
    return e
