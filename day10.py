from utils import Point, add_points, with_lines


@with_lines
def day10(lines):
    topomap, zeros = parse(lines)

    result_1 = sum(score(zero, topomap) for zero in zeros)

    result_2 = 0
    return result_1, result_2


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
