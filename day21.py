import itertools
from functools import cache

from utils import Point, with_lines


@with_lines
def day21(lines):
    # for line in lines:
    line = lines[0]
    line = line.split(':')[0]
    print(f'line: {line}')
    line = 'A' + line

    # Move robot 2 from A to line[0]
    # For each move in robot 2 moves move robot 1 from A to robot 2 move
    # Repeat for each move robot 2 makes

    # Make the robot 2 layer
    robot_2_paths: set[str] = {''}
    for src, dst in itertools.pairwise(line):
        print(f'{src} -> {dst}')
        new_paths = set()
        for seq in all_moves(NUMPAD_TO_POINT[dst], src=NUMPAD_TO_POINT[src]):
            for path in robot_2_paths:
                new_paths.add(path + seq + 'A')
        robot_2_paths = new_paths

    robot_1_paths: set[str] = set()
    for r1_line in robot_2_paths:
        r1_line = 'A' + r1_line
        base_paths: set[str] = {''}
        for src, dst in itertools.pairwise(r1_line):
            # print(f'{src} -> {dst}')
            new_paths = set()
            for seq in all_moves(DPAD_TO_POINT[dst], src=DPAD_TO_POINT[src]):
                for path in base_paths:
                    new_paths.add(path + seq + 'A')
            base_paths = new_paths
        for path in base_paths:
            robot_1_paths.add(path)

    manual_paths: set[str] = set()
    for m_line in robot_1_paths:
        m_line = 'A' + m_line
        base_paths: set[str] = {''}
        for src, dst in itertools.pairwise(m_line):
            # print(f'{src} -> {dst}')
            new_paths = set()
            for seq in all_moves(DPAD_TO_POINT[dst], src=DPAD_TO_POINT[src]):
                for path in base_paths:
                    new_paths.add(path + seq + 'A')
            base_paths = new_paths
        for path in base_paths:
            manual_paths.add(path)

    # for path in manual_paths:
    #     print(path)
    shortest_path = min(manual_paths, key=len)
    print(shortest_path)

    return 0, 0


NUMPAD = ['789', '456', '123', ' 0A']
NUMPAD_TO_POINT = {c: Point(x, y) for y, row in enumerate(NUMPAD) for x, c in enumerate(row)}
POINT_TO_NUMPAD = {v: k for k, v in NUMPAD_TO_POINT.items()}

DPAD = [' ^A', '<v>']
DPAD_TO_POINT = {c: Point(x, y) for y, row in enumerate(DPAD) for x, c in enumerate(row)}
POINT_TO_DPAD = {v: k for k, v in DPAD_TO_POINT.items()}


def expand(line: str, src=DPAD_TO_POINT['A'], prefixes: set[str] = None) -> set[str]:
    prefixes = {''} if prefixes is None else prefixes
    expanded = set()

    c, cdr = line[0], line[1:]
    dst = DPAD_TO_POINT[c]

    moves = all_moves(dst, src=src, and_key=True)

    for move in moves:
        for prefix in prefixes:
            expanded.add(prefix + move)

    if not cdr:
        return expanded

    return expand(cdr, src=dst, prefixes=expanded)


@cache
def all_moves(dst: Point, src: Point = DPAD_TO_POINT['A'], and_key: bool = False) -> set[str]:
    """
    return all possible paths on a pad that move from src to dst
    :param src: src point on the pad
    :param dst: dst point on the pad
    :param and_key: whether to include the key press in the path
    :return:
    """
    path = ''
    delta = dst - src

    if delta.x < 0:
        path += '<' * abs(delta.x)
    elif delta.x > 0:
        path += '>' * delta.x

    if delta.y < 0:
        path += '^' * abs(delta.y)
    elif delta.y > 0:
        path += 'v' * delta.y

    movesets = {''.join(p) for p in itertools.permutations(path)}
    if and_key:
        movesets = {m + 'A' for m in movesets}
    return movesets


DPAD_TO_DPAD_SEQUENCES = {
    '^': all_moves(DPAD_TO_POINT['^'], and_key=True),
    'v': all_moves(DPAD_TO_POINT['v'], and_key=True),
    '<': all_moves(DPAD_TO_POINT['<'], and_key=True),
    '>': all_moves(DPAD_TO_POINT['>'], and_key=True),
    'A': {'A'},
}


def test_all_moves():
    src = Point(1, 1)  # 5
    dst = Point(2, 3)  # A
    assert all_moves(dst, src) == {'>vv', 'v>v', 'vv>'}

    src = Point(2, 3)  # A
    dst = Point(0, 1)  # 8
    assert all_moves(dst, src) == {'<<^^', '<^<^', '<^^<', '^<<^', '^<^<', '^^<<'}


def test_dpad_to_point():
    assert DPAD_TO_POINT['^'] == Point(1, 0)
    assert DPAD_TO_POINT['v'] == Point(1, 1)
    assert DPAD_TO_POINT['<'] == Point(0, 1)
    assert DPAD_TO_POINT['>'] == Point(2, 1)
    assert DPAD_TO_POINT['A'] == Point(2, 0)


def test_numpad_to_point():
    assert NUMPAD_TO_POINT['7'] == Point(0, 0)
    assert NUMPAD_TO_POINT['8'] == Point(1, 0)
    assert NUMPAD_TO_POINT['9'] == Point(2, 0)
    assert NUMPAD_TO_POINT['4'] == Point(0, 1)
    assert NUMPAD_TO_POINT['5'] == Point(1, 1)
    assert NUMPAD_TO_POINT['6'] == Point(2, 1)
    assert NUMPAD_TO_POINT['1'] == Point(0, 2)
    assert NUMPAD_TO_POINT['2'] == Point(1, 2)
    assert NUMPAD_TO_POINT['3'] == Point(2, 2)
    assert NUMPAD_TO_POINT['0'] == Point(1, 3)
    assert NUMPAD_TO_POINT['A'] == Point(2, 3)


def test_dpad_to_txt():
    output = [
        [' '] * 3,
        [' '] * 3
    ]
    for y in range(2):
        for x in range(3):
            output[y][x] = POINT_TO_DPAD[Point(x, y)]

    s = '\n'.join([''.join(o) for o in output])
    print(s)

    assert s == ' ^A\n<v>'


def test_numpad_to_txt():
    output = [
        [' '] * 3,
        [' '] * 3,
        [' '] * 3,
        [' '] * 3,
    ]
    for y in range(4):
        for x in range(3):
            output[y][x] = POINT_TO_NUMPAD[Point(x, y)]

    s = '\n'.join([''.join(o) for o in output])
    print(s)

    assert s == '789\n456\n123\n 0A'
