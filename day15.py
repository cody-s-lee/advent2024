from enum import Enum, StrEnum
from typing import Tuple

from point import E, N, Point, S, W
from utils import with_content


@with_content
def day15(content):
    wh = Warehouse.parse(content)

    print(wh)
    wh.execute()
    print(wh)

    result_a = wh.gps()

    print(f'\n{"-" * 120}\n')

    wh = Warehouse.parse(e_x_p_a_n_d(content))

    print(wh)
    wh.execute()
    print(wh)

    result_b = wh.gps()

    return result_a, result_b


def e_x_p_a_n_d(content: str) -> str:
    return content.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')


class Warehouse:
    def __init__(self, map_lines: list[list[chr]], map_size: Tuple[int, int], robot_moves: str, robot_pos: Point):
        self.map_lines = map_lines
        self.map_size = map_size
        self.robot_moves = robot_moves
        self.robot_pos = robot_pos

    @classmethod
    def parse(cls, content: str):
        map_str, robot_moves = content.split('\n\n')
        map_lines = [[c for c in line] for line in map_str.splitlines()]
        map_width, map_height = len(map_lines[0]), len(map_lines)
        robot_pos = None

        for y, line in enumerate(map_lines):
            for x, char in enumerate(line):
                if char == '@':
                    robot_pos = Point(x, y)
                    break
        assert robot_pos is not None, 'Robot not found'

        return cls(map_lines, (map_width, map_height), robot_moves.replace('\n', ''), robot_pos)

    def __str__(self):
        s = f'Warehouse {self.map_size[0]}x{self.map_size[1]}, robot at {self.robot_pos}\n'
        return s + '\n'.join([''.join(line) for line in self.map_lines])

    def at(self, pos: Point):
        return self.CellType(self.map_lines[pos.y][pos.x])

    class Direction(Enum):
        UP = U = ('^', N)
        DOWN = D = ('v', S)
        LEFT = L = ('<', W)
        RIGHT = R = ('>', E)

        @classmethod
        def of(cls, char):
            for dir in cls:
                if dir.value[0] == char:
                    return dir

    class CellType(StrEnum):
        WALL = W = '#'
        EMPTY = E = '.'
        BOX = B = 'O'
        BOX_LEFT = L = '['
        BOX_RIGHT = R = ']'
        ROBOT = X = '@'

        def as_char(self) -> chr:
            assert len(self) == 1
            return self.value[0]

    def _move(self, dir) -> bool:
        if dir not in self.Direction:
            raise ValueError(f'Invalid direction {dir}')

        open = {self.robot_pos}
        closed = set()

        move = set()
        updates = {self.robot_pos: self.CellType.EMPTY}

        while open:
            src = open.pop()

            if src in closed:
                continue

            match self.at(src):
                case self.CellType.WALL:
                    return False
                case self.CellType.BOX | self.CellType.ROBOT:
                    move.add(src)
                    open.add(src + dir.value[1])
                case self.CellType.BOX_LEFT:
                    move.add(src)
                    open.add(src + dir.value[1])
                    pair_pos = src + self.Direction.RIGHT.value[1]
                    open.add(pair_pos)
                    updates[pair_pos] = self.CellType.EMPTY
                case self.CellType.BOX_RIGHT:
                    move.add(src)
                    open.add(src + dir.value[1])
                    pair_pos = src + self.Direction.LEFT.value[1]
                    open.add(pair_pos)
                    updates[pair_pos] = self.CellType.EMPTY

            closed.add(src)

        for pos in move:
            updates[pos + dir.value[1]] = self.at(pos)

        for pos, ct in updates.items():
            self.map_lines[pos.y][pos.x] = ct.as_char()

        self.robot_pos += dir.value[1]

        return True

    def execute(self):
        for move in self.robot_moves:
            # print(f'Executing move {move}')
            self._move(self.Direction.of(move))
            # print(self)

    def gps(self, pos=None) -> int:
        width, height = self.map_size

        if pos is None:
            return sum(self.gps(Point(x, y)) for x in range(width) for y in range(height) if
                       self.at(Point(x, y)) in (self.CellType.BOX, self.CellType.BOX_LEFT))

        return pos.x + 100 * pos.y
