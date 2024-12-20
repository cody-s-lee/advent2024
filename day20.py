from collections import defaultdict

from utils import CARDINAL_DIRECTIONS, Point, is_example, with_lines


@with_lines
def day20(lines: list[str]) -> tuple[int, int]:
    src, dst, points, edges = parse(lines)

    # build dist map from src to all points
    dist_src_x = gen_dist_map(src, edges)

    # build dist map from all points to dst
    dist_x_dst = gen_dist_map(dst, edges)

    assert dist_src_x[dst] == dist_x_dst[src]

    base = dist_src_x[dst]

    shortcut_counter, shortcuts = make_shortcuts(base, dist_src_x, dist_x_dst, points, 2)

    print(f'Num of shortcuts: {len(shortcuts)}')
    print(f'Base: {base}')

    if is_example():
        for i in sorted(shortcut_counter.keys()):
            if shortcut_counter[i] > 0:
                print(f'{i}: {shortcut_counter[i]}')

    result_a = 0
    for (p, q), d in shortcuts.items():
        # print(f'{p} -> {q} ({d})')
        if d + 100 <= base:
            # print(f'Found good shortcut! {p} -> {q} ({d})')
            result_a += 1

    return result_a, 0


def make_shortcuts(base, dist_src_x, dist_x_dst, points, cheat_length: int):
    shortcuts: [dict[tuple[Point, Point], int]] = dict()  # (p, q) -> dist
    shortcut_counter = defaultdict(int)
    # for every pair of points p,q surrounding a wall
    # if dist(src, p) + 2 + dist(q, dst) <= base it's a good shortcut
    for p in points:
        for q in [q for q in p.within_dist(cheat_length) if q in points and p.dist(q) > 1]:
            dist = dist_src_x[p] + cheat_length + dist_x_dst[q]
            if dist < base:
                # print(f'Found shortcut: {p} -> {q}')
                shortcuts[(p, q)] = dist
                shortcut_counter[base - dist] += 1

            pass
    return shortcut_counter, shortcuts


def gen_dist_map(src, edges):
    dist = defaultdict(lambda: 10 ** 9)
    dist[src] = 0
    queue = [src]
    while queue:
        u = queue.pop(0)
        for edge in edges[u]:
            v = edge.dst
            alt = dist[u] + edge.weight
            if alt < dist[v]:
                dist[v] = alt
                queue.append(v)

    return dist


class Edge:
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __hash__(self):
        return hash((self.src, self.dst, self.weight))

    def __repr__(self):
        return f'{self.src} -> {self.dst} ({self.weight})'


def parse(lines: list[str]) -> tuple[Point, Point, set[Point], dict[Point, set[Edge]]]:
    src = None
    dst = None
    points = set()
    edges = defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in '.SE':
                p = Point(x, y)
                points.add(p)
                if c == 'S':
                    src = p
                elif c == 'E':
                    dst = p

    for p in points:
        for d in CARDINAL_DIRECTIONS:
            q = p + d
            if q in points:
                edges[p].add(Edge(p, q, 1))
                edges[q].add(Edge(q, p, 1))

    assert src is not None
    assert dst is not None

    return src, dst, points, edges


if __name__ == '__main__':
    filename = f'day20{"example" if is_example() else ""}.txt'

    # Execute
    with open(filename, 'r') as file:
        result_a, result_b = day20(file.read())
        print(f'Results: {result_a}, {result_b}')
