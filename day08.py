from collections import defaultdict
from copy import copy

from utils import Point, with_lines


@with_lines
def day08(lines):
    grid = dict()
    frequencies = defaultdict(set)
    for y, line in enumerate(lines):
        for x, f in enumerate(line):
            grid[Point(x, y)] = f

            if f == '.':
                continue

            frequencies[f].add(Point(x, y))

    print('-' * 80)
    print(grid_str(grid))
    print('-' * 80)

    antinodes_a, antinodes_b = set(), set()
    for frequency_set in frequencies.values():
        # for each pair of points in the set, add the antinode
        for q in frequency_set:
            for r in frequency_set:
                if q == r:
                    continue

                a = find_antinodes(q, r, grid, all=False)
                antinodes_a.update(a)

                b = find_antinodes(q, r, grid, all=True)
                antinodes_b.update(b)

    g_a = {p: '#' for p in antinodes_a}
    g_b = {p: '#' for p in antinodes_b}

    print(grid_str(g_a))
    print('-' * 80)
    print(grid_str(g_b))
    print('-' * 80)

    result_a, result_b = len(antinodes_a), len(antinodes_b)

    return result_a, result_b


def find_antinodes(p1, p2, grid, all=False):
    antinodes = {p2} if all else {}
    dx, dy = p2.x - p1.x, p2.y - p1.y

    a = p2
    while True:
        a = Point(a.x + dx, a.y + dy)

        if a not in grid:
            break

        if not all:
            return {a}

        antinodes.add(a)

    return antinodes


def grid_str(grid):
    g = copy(grid)

    min_x = min(p.x for p in g)
    max_x = max(p.x for p in g)
    min_y = min(p.y for p in g)
    max_y = max(p.y for p in g)

    s = ''
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            s += g.get(Point(x, y), '.')
        s += '\n'

    return s
