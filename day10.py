from point import Point, add_points
from utils import with_lines


@with_lines
def day10(lines):
    topomap, zeros = parse(lines)

    result_1 = sum(score(zero, topomap) for zero in zeros)
    result_2 = sum(rating(zero, topomap) for zero in zeros)

    return result_1, result_2


def to_str(path: list[Point], topomap: dict[Point, int]) -> str:
    p = path.pop(0)
    print(p)
    s = f'({topomap[p]}@{p.x},{p.y})'

    while path:
        p = path.pop(0)
        s += f'->({topomap[p]}@{p.x},{p.y})'

    return s


def parse(lines) -> tuple[dict[Point, int], set[Point]]:
    topomap = dict()
    zeros = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            value = int(char)
            topomap[Point(x, y)] = value
            if value == 0:
                zeros.add(Point(x, y))

    return topomap, zeros


def score(start, topomap):
    nines = find_nines(start, topomap)
    return len(nines)


def rating(start, topomap):
    paths = find_paths(start, topomap)
    # for path in paths:
    #     print(f'{to_str(list(path), topomap)}')
    return len(paths)


def find_paths(point, topomap):
    value = topomap[point]
    if value == 9:
        return [[point]]

    paths = []
    for direction in [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]:
        step = add_points(point, direction)
        if step in topomap and topomap[step] == value + 1:
            for path in find_paths(step, topomap):
                paths.append([point] + path)

    return paths


def find_nines(point, topomap):
    # find adjacent tiles that increase in elevation by one
    value = topomap[point]
    if value == 9:
        return {point}

    steps = set()
    for direction in [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]:
        step = add_points(point, direction)
        if step in topomap and topomap[step] == value + 1:
            steps.update(find_nines(step, topomap))

    return steps
