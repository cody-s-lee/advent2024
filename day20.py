from collections import defaultdict
from functools import cache

from sortedcontainers import SortedList

from utils import CARDINAL_DIRECTIONS, Point, with_content

LEVELS = [(2, '2'), (1, '1')]


@with_content
def day20(content: str) -> tuple[int, int]:
    base = fastest_path(content, extract(content), allow_tunnelling=False)

    return 0, 0


@cache
def fastest_path(maze: str, allow_tunnelling=True) -> int:
    # implement Dijkstra's algorithm
    start = (maze, extract(maze))

    dist = defaultdict(10 ** 9)
    dist[start] = 0

    prev = defaultdict(None)

    queue = SortedList([start], key=lambda x: dist[x])

    while queue:
        u = queue.pop(0)
        maze, pos = u

        if at(maze, pos) == 'E':
            return dist[u]

        for v in neighbors(maze, pos, allow_tunnelling=allow_tunnelling):
            alt = dist[u] + 1

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                queue.add(v)


@cache
def neighbors(maze: str, pos: Point, allow_tunnelling) -> list[tuple[str, Point]]:
    width, height = dimensions(maze)

    n_pos = [pos + d for d in CARDINAL_DIRECTIONS if 0 <= pos.x + d.x < width - 1 and 0 <= pos.y + d.y < height]
    l = level(maze)

    if l == 2:  # used up all quantum tunneling, no shenanigans
        return [(maze, p) for p in n_pos if maze[index(p, width)] in '.E']
    elif l == 1:  # currently quantum tunneling
        return [(replace(maze, index(pos, width), '2'), p) for p in n_pos if at(maze, p) in '.E']
    else:  # no quantum tunneling used yet
        neighbors = []
        for p in n_pos:
            if allow_tunnelling and at(maze, p) == '#':
                neighbors.append(replace(maze, index(pos, width), '1'), p)
            else:
                neighbors.append((maze, p))
        return neighbors


@cache
def at(maze: str, pos: Point) -> str:
    return maze[index(pos, dimensions(maze)[0])]


@cache
def level(maze: str) -> int:
    for i, n in LEVELS:
        if n in maze:
            return i
    return 0


@cache
def index(pos, width):
    return pos.y * width + pos.x


@cache
def dimensions(maze: str) -> tuple[int, int]:
    """
    Returns the width and height of the maze including newlines
    Maze must end with a newline
    :param maze: maze string
    :return: width, height
    """
    return maze.index('\n') + 1, maze.count('\n')


@cache
def extract(maze: str, mouse='S') -> Point:
    width, _ = dimensions(maze)

    idx = maze.find(mouse)
    return Point(idx % width, idx // width)


@cache
def replace(maze, idx, char='.'):
    if type(idx) is Point:
        idx = index(idx, dimensions(maze)[0])
    return maze[:idx] + char + maze[idx + 1:]
