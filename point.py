import typing
from enum import Enum


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

    def within_dist(self, dist):
        for x in range(-dist, dist + 1):
            for y in range(-dist, dist + 1):
                if abs(x) + abs(y) <= dist:
                    yield Point(self.x + x, self.y + y)


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
