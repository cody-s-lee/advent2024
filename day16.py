from collections import defaultdict
from typing import NamedTuple, Optional

from sortedcontainers import SortedList

from utils import Direction, NEXT_DIRECTION, PREV_DIRECTION, Point, with_lines


@with_lines
def day16(lines):
    grid, start, end = parse(lines)

    _, result_a = dijkstra(grid, start, end, Direction.EAST.value)
    paths, _ = dijkstrall(grid, start, end, Direction.EAST.value)

    result_b = len({node.pos for path in paths for node in path})

    return result_a, result_b


class Node(NamedTuple):
    pos: Point
    facing: Point

    def __eq__(self, other):
        return self.pos == other.pos and self.facing == other.facing

    def __hash__(self):
        return hash((self.pos, self.facing))

    def __lt__(self, other):
        return self.pos < other.pos or (self.pos == other.pos and self.facing < other.facing)


def dijkstra(grid, start, end, facing) -> tuple[list[Node], int]:
    # find shortest path on the grid
    # movement costs 1
    # rotation costs 1000
    # state is (x, y, f)
    # f is the direction the reindeer is facing
    # use dijkstra's algorithm

    dist: dict[Node, int] = defaultdict(lambda: 10 ** 9)
    prev: dict[Node, Optional[Node]] = defaultdict(lambda: None)
    dist[Node(start, facing)] = 0
    queue: SortedList[Node] = SortedList(key=lambda x: dist[x])
    queue.add(Node(start, facing))
    closed = set()

    while queue:
        u = queue.pop(0)
        if u in closed:
            continue
        closed.add(u)

        # test rotations
        for f, cost in [(ND[u.facing], 1000), (ND[ND[u.facing]], 2000), (PD[u.facing], 1000)]:
            v = Node(u.pos, f)
            alt = dist[u] + cost
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                queue.add(v)
                closed.discard(v)

        # test forward neighbor
        v = Node(u.pos + u.facing, u.facing)
        if grid[v.pos.y][v.pos.x] in '.SE':
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                queue.add(v)
                closed.discard(v)

    best = Node(end, Direction.E.value)
    for f in Direction:
        if dist[Node(end, f.value)] < dist[best]:
            best = Node(end, f.value)

    u = best
    path = [u]
    while prev[u]:
        u = prev[u]
        path.insert(0, u)

    return path, dist[best]


def dijkstrall(grid, start, end, facing) -> tuple[list[list[Node]], int]:
    # find shortest path on the grid
    # movement costs 1
    # rotation costs 1000
    # state is (x, y, f)
    # f is the direction the reindeer is facing
    # use dijkstra's algorithm

    dist: dict[Node, int] = defaultdict(lambda: 10 ** 9)
    prev: dict[Node, Optional[set[Node]]] = defaultdict(lambda: set())
    dist[Node(start, facing)] = 0
    queue: SortedList[Node] = SortedList(key=lambda x: dist[x])
    queue.add(Node(start, facing))
    closed = set()

    while queue:
        u = queue.pop(0)
        if u in closed:
            continue
        closed.add(u)

        # test rotations
        for f, cost in [(ND[u.facing], 1000), (ND[ND[u.facing]], 2000), (PD[u.facing], 1000)]:
            v = Node(u.pos, f)
            alt = dist[u] + cost
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = {u}
                queue.add(v)
                closed.discard(v)
            elif alt == dist[v]:
                prev[v].add(u)

        # test forward neighbor
        v = Node(u.pos + u.facing, u.facing)
        if grid[v.pos.y][v.pos.x] in '.SE':
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = {u}
                queue.add(v)
                closed.discard(v)
            elif alt == dist[v]:
                prev[v].add(u)

    end_score = 10 ** 9
    ends = []
    for f in Direction:
        score = dist[Node(end, f.value)]
        if score < end_score:
            end_score = score
            ends = [Node(end, f.value)]
        elif score == end_score:
            ends.append(Node(end, f.value))

    paths = [[end] for end in ends]
    path_queue = paths[:]
    full_paths = []
    while path_queue:
        path = path_queue.pop(0)
        u = path[0]
        if u.pos == start:
            full_paths.append(path)
        for v in prev[u]:
            path_queue.append([v] + path)

    return full_paths, end_score


# Rotations
ND = NEXT_DIRECTION
PD = PREV_DIRECTION


def parse(lines):
    grid = []
    start, end = None, None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'S':
                start = Point(x, y)
            elif c == 'E':
                end = Point(x, y)
        grid.append([c for c in line])
    assert start is not None
    assert end is not None

    return grid, start, end
