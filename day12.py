from utils import CARDINAL_DIRECTIONS, E, N, Point, S, W, add_points, neighbors, one_of, with_lines

Region = set[Point]


@with_lines
def day12(lines):
    garden = parse(lines)
    regions: list[Region] = []
    region_map: dict[Point, Region] = dict()

    for p, c in garden.items():
        if p in region_map:
            continue

        queue = [p]
        region = set()
        regions.append(region)
        while queue:
            q = queue.pop()
            if q in region:
                continue
            region.add(q)
            region_map[q] = region
            for n in neighbors(q):
                if n in garden and garden[n] == c:
                    queue.append(n)

    result_a = sum(price(r) for r in regions)
    result_b = sum(area(r) * sides(r) for r in regions)

    for r in regions:
        p = one_of(r)
        print(f'Region {garden[p]} starting at {p} with area {area(r)} and sides {sides(r)}')

    return result_a, result_b


def price(region: set[Point]) -> int:
    return area(region) * perimeter(region)


def area(region: set[Point]) -> int:
    return len(region)


def perimeter(region: set[Point]) -> int:
    return sum(sum(1 for n in neighbors(p) if n not in region) for p in region)


NEXT_DIRECTION = {
    N: E,
    E: S,
    S: W,
    W: N
}


def sides(region: set[Point]) -> int:
    # like perimeter but if my neighbor to the E has a N fence, my N fence doesn't count
    # For N fence -> E neighbor, for E fence -> S neighbor, for S fence -> W neighbor, for W fence -> N neighbor
    num_sides = 0
    for p in region:
        for d in CARDINAL_DIRECTIONS:
            e = NEXT_DIRECTION[d]
            n = add_points(p, e)
            if n in region and add_points(n, d) not in region:
                continue
            if add_points(p, d) not in region:
                num_sides += 1

    return num_sides


def parse(lines: list[str]) -> dict[Point, str]:
    garden = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            garden[Point(x, y)] = c
    return garden
