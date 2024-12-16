import re
from collections import defaultdict
from copy import copy

from utils import CARDINAL_DIRECTIONS, Point, is_example, neighbors, with_lines


@with_lines
def day14(lines):
    lobby = Lobby.parse(lines)

    if is_example():
        assert lobby.width == 11
        assert lobby.height == 7
    else:
        assert lobby.width == 101
        assert lobby.height == 103

    safety_factor_100 = None

    n = 0
    min_safety_factor = 10000000000
    min_safety_time = 0
    str_safety_score = str(lobby)
    for _ in range(10000):
        n += 1
        lobby.tick()

        safety_factor = lobby.safety_factor
        if safety_factor < min_safety_factor:
            min_safety_time = n
            min_safety_factor = safety_factor
            str_safety_score = str(lobby)

        if n == 100:
            safety_factor_100 = safety_factor

    print(str_safety_score)

    return safety_factor_100, min_safety_time


class Lobby:
    def __init__(self, width: int, height: int, robots: set = None):
        self._width = width
        self._height = height
        if robots is None:
            robots = set()
        self._robots = robots

    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                c = self.count_at(Point(x, y))
                s += f'{c:x}' if c else '.'
            s += '\n'
        return s

    def count_at(self, pos: Point):
        n = 0
        for robot in self._robots:
            if robot.pos == pos:
                n += 1
        return n

        # return sum(1 for robot in self._robots if robot.pos == pos)

    @property
    def safety_factor(self):
        safety_factor = 1
        for q_count in self.count_quadrants().values():
            safety_factor *= q_count
        return safety_factor

    @property
    def robots(self):
        return copy(self._robots)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @classmethod
    def parse(cls, lines):
        robots = set()
        lobby = cls(1, 1, robots)
        max_x, max_y = 0, 0
        for line in lines:
            robot = Robot.parse(line, lobby)
            if robot.pos.x > max_x:
                max_x = robot.pos.x
            if robot.pos.y > max_y:
                max_y = robot.pos.y
            robots.add(robot)
        lobby._width = max_x + 1
        lobby._height = max_y + 1
        return lobby

    def tick(self):
        for robot in self._robots:
            robot.step()

    @property
    def t_l(self):
        p = Point
        lw = self.width
        lh = self.height

        return p(0, 0), p(lw // 2, lh // 2)

    @property
    def t_r(self):
        p = Point
        lw = self.width
        lh = self.height

        return p(lw // 2 + 1, 0), p(lw, lh // 2)

    @property
    def b_l(self):
        p = Point
        lw = self.width
        lh = self.height

        return p(0, lh // 2 + 1), p(lw // 2, lh)

    @property
    def b_r(self):
        p = Point
        lw = self.width
        lh = self.height

        return p(lw // 2 + 1, lh // 2 + 1), p(lw, lh)

    def count_quadrants(self):
        quadrant_coords = [self.t_l, self.t_r, self.b_l, self.b_r]

        counts = defaultdict(int)
        for q in quadrant_coords:
            min_c, max_c = q
            count = 0

            for robot in self.robots:
                if min_c.x <= robot.pos.x < max_c.x and min_c.y <= robot.pos.y < max_c.y:
                    count += 1

            counts[q] = count

        return counts

    def q_map(self):
        q_counts = self.count_quadrants()
        s = (f'{q_counts[self.t_l]:x} {q_counts[self.t_r]:x}\n'
             f'{q_counts[self.b_l]:x} {q_counts[self.b_r]:x}')
        return s

    def has_tree(self):
        for robot in self.robots:
            for p in neighbors(robot.pos, directions=CARDINAL_DIRECTIONS):
                if self.count_at(p) == 0:
                    return False

        return True


class Robot:
    PARSER = re.compile(r'p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)')

    def __init__(self, pos: Point, vel: Point, lobby: Lobby):
        self._pos = pos
        self._vel = vel
        self._lobby = lobby

    @property
    def pos(self):
        return self._pos

    def step(self):
        self._pos = Point((self._pos.x + self._vel.x) % self._lobby.width,
                          (self._pos.y + self._vel.y) % self._lobby.height)

    @classmethod
    def parse(cls, line: str, lobby: Lobby):
        p_x, p_y, v_x, v_y = cls.PARSER.match(line).groups()
        pos = Point(int(p_x), int(p_y))
        vel = Point(int(v_x), int(v_y))
        return cls(pos, vel, lobby)
