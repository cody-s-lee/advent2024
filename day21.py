import itertools
from functools import cache

from point import Point
from utils import with_lines


@with_lines
def day21(lines):
    result_a = part_nx(lines, 2)
    result_b = part_nx(lines, 25)

    return result_a, result_b


def part_nx(lines, n=2):
    result = 0
    for line in lines:
        line = line.split(':')[0]
        # line = '179A'
        # print(f'line: {line}')
        line = 'A' + line

        # Make the robot 2 layer
        paths: set[str] = {''}
        for src, dst in itertools.pairwise(line):
            # print(f'{src} -> {dst}')
            new_paths = set()
            for seq in all_moves(NUMPAD_TO_POINT[dst], src=NUMPAD_TO_POINT[src], is_dpad=False):
                for path in paths:
                    new_paths.add(path + seq + 'A')
            paths = new_paths
        ### Good up until here

        min_path_cost = 10 ** 20
        for path in paths:
            path_parts = explode(path)
            part_costs = [0] * len(path_parts)
            for i, part in enumerate(path_parts):
                part_costs[i] = cost(part, n)
            path_cost = sum(part_costs)
            if path_cost < min_path_cost:
                min_path_cost = path_cost

        result += min_path_cost * int(line[1:-1], 10)
    return result


@cache
def cost(seq, depth):
    if depth == 0:
        return len(seq)

    sub_sequences = redirect_part(seq)
    sub_sequence_costs = [10 ** 20] * len(sub_sequences)

    for i, part in enumerate(sub_sequences):
        sub_parts = explode(part)
        sub_part_costs = [cost(sub_part, depth - 1) for sub_part in sub_parts]
        sub_sequence_costs[i] = sum(sub_part_costs)

    return min(sub_sequence_costs)


@cache
def explode(path: str) -> list[str]:
    return [p + 'A' for p in path[:-1].split('A')]


@cache
def redirect_part(path_part: str) -> set[str]:
    """
    create all optimal length redirected paths for A + path_part + A
    :param path_part:
    :return:
    """
    paths: set[str] = set()
    line = 'A' + path_part

    base_paths: set[str] = {''}
    # min_path_len = 10 ** 9
    for src, dst in itertools.pairwise(line):
        new_paths = set()
        for seq in all_moves(DPAD_TO_POINT[dst], src=DPAD_TO_POINT[src]):
            for path in base_paths:
                new_paths.add(path + seq + 'A')
        base_paths = new_paths
    for path in base_paths:
        # if len(path) > min_path_len:
        #     continue
        # elif len(path) < min_path_len:
        #     min_path_len = len(path)
        #     paths.clear()
        paths.add(path)

    return paths


def redirect_path(path: str) -> set[str]:
    path_parts = explode(path[:-1])
    redirected_parts: list[set[str]] = [redirect_part(part) for part in path_parts]
    paths = {''}
    for part in redirected_parts:
        paths = {''.join(q) for q in itertools.product(paths, part)}

    return paths


def redirect_paths(paths: set[str]) -> set[str]:
    return {path for p in paths for path in redirect_path(p)}


def redirect(robot_2_paths):
    # Make the robot 1 layer
    robot_1_paths: set[str] = set()
    for r1_line in robot_2_paths:
        r1_line = 'A' + r1_line
        base_paths: set[str] = {''}
        for src, dst in itertools.pairwise(r1_line):
            # print(f'{src} -> {dst}')
            new_paths = set()
            best_seq_len = 10 ** 9
            for seq in all_moves(DPAD_TO_POINT[dst], src=DPAD_TO_POINT[src]):
                if len(seq) < best_seq_len:
                    best_seq_len = len(seq)
                    new_paths.clear()
                for path in base_paths:
                    new_paths.add(path + seq + 'A')
            base_paths = new_paths
        for path in base_paths:
            robot_1_paths.add(path)
    return robot_1_paths


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
def all_moves(dst: Point, src: Point = DPAD_TO_POINT['A'], and_key: bool = False, is_dpad=True) -> set[str]:
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
    if delta.y > 0:
        path += 'v' * delta.y
    if delta.y < 0:
        path += '^' * abs(delta.y)
    if delta.x > 0:
        path += '>' * delta.x

    movesets = {path for path in {''.join(p) for p in itertools.permutations(path)} if is_valid(path, src, is_dpad)}

    if and_key:
        movesets = {m + 'A' for m in movesets}
    return movesets


def is_valid(path: str, src: Point, is_dpad=True) -> bool:
    pos = src
    for c in path:
        match c:
            case '^':
                pos = pos + Point(0, -1)
            case 'v':
                pos = pos + Point(0, 1)
            case '<':
                pos = pos + Point(-1, 0)
            case '>':
                pos = pos + Point(1, 0)

        if is_dpad:
            if POINT_TO_DPAD[pos] == ' ':  # out of bounds
                return False
        else:
            if POINT_TO_NUMPAD[pos] == ' ':  # out of bounds
                return False
    return True


def test_is_invalid():
    path = '<<v'
    src = DPAD_TO_POINT['A']

    assert not is_valid(path, src, is_dpad=True)


def test_all_moves():
    src = Point(1, 1)  # 5
    dst = Point(2, 3)  # A
    assert all_moves(dst, src, is_dpad=False) == {'>vv', 'v>v', 'vv>'}

    src = Point(2, 3)  # A
    dst = Point(0, 1)  # 8
    assert all_moves(dst, src, is_dpad=False) == {'<<^^', '<^<^', '<^^<', '^<<^', '^<^<', '^^<<'}


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
