from collections import defaultdict
from functools import cache, lru_cache

from sortedcontainers import SortedList

from utils import CARDINAL_DIRECTIONS, Point, is_example, with_content


@cache
def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@with_content
def day20(content: str) -> tuple[int, int]:
    src = extract(content, 'S')
    dst = extract(content, 'E')
    base = fastest_path_astar(content, src, dst)

    fast_fail = base - 99 if not is_example() else None  # fail if path is longer than fast_fail
    tunneled_mazes = make_tunneled_mazes(content, base if is_example() else (base - 100))

    print(f'Num of tunneled mazes: {len(tunneled_mazes)}')

    result_a = 0
    savings = defaultdict(int)
    i = 0
    for tm in tunneled_mazes:
        i += 1
        print(f'\rProcessing maze {i}', end='')

        one = extract(tm, '1')
        two = extract(tm, '2')
        if not is_example():
            if manhattan_distance(src, one) + manhattan_distance(one, dst) + 100 > base:
                continue

        delta = base - (fastest_path_astar(tm, src, one, fast_fail) + 1 + fastest_path_astar(tm, two, dst, fast_fail))

        if delta > 0:
            savings[delta] += 1
        if delta >= 100:
            result_a += delta

    print()

    for i in sorted(savings.keys()):
        if savings[i] > 0:
            print(f'{i}: {savings[i]}')

    return result_a, 0


def make_tunneled_mazes(maze: str, base: int) -> list[str]:
    width, height = dimensions(maze)
    src, dst = extract(maze, 'S'), extract(maze, 'E')
    tunneled_mazes = []

    i = 0
    for y in range(1, height):
        for x in range(1, width - 1):
            p = Point(x, y)
            if at(maze, p) == '#':  # walking through a wall
                tm = replace(maze, p, '.')
                i += 1
                print(f'\rVerifying maze {i}', end='')
                if fastest_path_astar(tm, src, p) + fastest_path_astar(tm, p, dst) <= base:
                    for d in CARDINAL_DIRECTIONS:
                        if 0 <= x + d.x < width - 1 and 0 <= y + d.y < height and at(maze, p + d) in '.E':
                            tunneled_mazes.append(replace(replace(tm, p, '1'), p + d, '2'))
    print()

    return tunneled_mazes


def make_tunnelling_mazes(maze: str) -> list[str]:
    width, height = dimensions(maze)

    tunnelling_mazes = []

    for y in range(height):
        for x in range(width):
            p = Point(x, y)
            if at(maze, p) == '#':  # walking through a wall
                for d in CARDINAL_DIRECTIONS:
                    if 0 <= x + d.x < width - 1 and 0 <= y + d.y < height and at(maze,
                                                                                 p + d) in '.E':  # to an empty space or the exit
                        tunnelling_mazes.append(replace(replace(maze, p, '1'), p + d, '2'))

    return tunnelling_mazes


def fastest_path(maze: str, src: Point, dst: Point, fast_fail: [int | None] = None) -> int:
    # implement Dijkstra's algorithm
    dist = defaultdict(lambda: 10 ** 9)
    dist[src] = 0

    prev = defaultdict(None)

    queue = SortedList([src], key=lambda x: dist[x])

    while queue:
        u = queue.pop(0)

        if u == dst:
            return dist[u]

        for v in neighbors(maze, u):
            alt = dist[u] + 1

            if fast_fail is not None and alt > fast_fail:
                continue

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                queue.add(v)

    return 10 ** 9


def fastest_path_astar(maze: str, src: Point, dst: Point, fast_fail: [int | None] = None) -> int:
    def heuristic(a: Point, b: Point) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    dist = defaultdict(lambda: 10 ** 9)
    dist[src] = 0

    queue = SortedList([src], key=lambda x: dist[x] + heuristic(x, dst))

    while queue:
        u = queue.pop(0)

        if u == dst:
            return dist[u]

        for v in neighbors(maze, u):
            alt = dist[u] + 1

            if fast_fail is not None and alt > fast_fail:
                continue

            if alt < dist[v]:
                dist[v] = alt
                queue.add(v)

    return 10 ** 9


def neighbors(maze: str, pos: Point) -> list[Point]:
    width, height = dimensions(maze)

    return [pos + d for d in CARDINAL_DIRECTIONS if
            0 <= pos.x + d.x < width - 1 and 0 <= pos.y + d.y < height and (
                    (at(maze, pos) in '.S' and at(maze, pos + d) in '.1E') or
                    (at(maze, pos) == '1' and at(maze, pos + d) in '2') or
                    (at(maze, pos) == '2' and at(maze, pos + d) in '.E')
            )]


@lru_cache
def at(maze: str, pos: Point) -> str:
    return maze[index(pos, dimensions(maze).x)]


@lru_cache
def index(pos: Point, width: int) -> int:
    return pos.y * width + pos.x


@lru_cache
def dimensions(maze: str) -> Point:
    """
    Returns the width and height of the maze including newlines
    Maze must end with a newline
    :param maze: maze string
    :return: width, height
    """
    return Point(maze.index('\n') + 1, maze.count('\n'))


def extract(maze: str, mouse: str = 'S') -> Point:
    width, _ = dimensions(maze)

    idx = maze.find(mouse)
    return Point(idx % width, idx // width)


def replace(maze: str, idx: [int | Point], char: str = '.'):
    if type(idx) is Point:
        idx = index(idx, dimensions(maze)[0])
    return maze[:idx] + char + maze[idx + 1:]


# test
def example():
    content = '###############\n#...#...#.....#\n#.#.#.#.#.###.#\n#S#...#.#.#...#\n#######.#.#.###\n#######.#.#...#\n#######.#.###.#\n###..E#...#...#\n###.#######.###\n#...###...#...#\n#.#####.#.###.#\n#.#...#.#.#...#\n#.#.#.#.#.#.###\n#...#...#...###\n###############\n'

    src = extract(content, 'S')
    dst = extract(content, 'E')

    base = fastest_path(content, src, dst)

    tunneled_mazes = make_tunnelling_mazes(content)

    print(f'Num of tunneled mazes: {len(tunneled_mazes)}')

    for tm in tunneled_mazes:
        # print(tm)
        td = fastest_path(tm, src, dst)
        if base - td == 2:
            print(tm)
            print()
            print('-' * 20)
            print()
            continue


if __name__ == '__main__':
    example()
