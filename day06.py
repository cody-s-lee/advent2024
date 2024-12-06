from collections import namedtuple

from utils import Point, add_points, with_lines

### Notes:
## "Smart"
# [  9:48AM ]  [ cody@Nitrogen:~/PycharmProjects/advent2024(main✗) ]
#  $ time python main.py 6
# Results: 4647, 1723
# Day 6 results: (4647, 1723)
# python main.py 6  89.85s user 0.45s system 99% cpu 1:31.18 total
## "Brute"
# [  9:50AM ]  [ cody@Nitrogen:~/PycharmProjects/advent2024(main✗) ]
#  $ time python main.py 6
# Brute: 1723, Smart: 0
# Results: 4647, 1723
# Day 6 results: (4647, 1723)
# python main.py 6  62.01s user 0.16s system 99% cpu 1:02.37 total;.


EMPTY = 0
WALL = -1

N = -2
E = -3
S = -4
W = -5

FACS = {N, E, S, W}

VECTOR = {
    N: Point(0, -1),
    E: Point(1, 0),
    S: Point(0, 1),
    W: Point(-1, 0),
}

NEXT = {
    N: E,
    E: S,
    S: W,
    W: N,
}

PREV = {
    E: N,
    S: E,
    W: S,
    N: W,
}

GuardState = namedtuple('GuardState', ['loc', 'fac'])


@with_lines
def day06(lines):
    grid = dict()

    guard_state = None
    guard_states = set()

    for y, v in enumerate(lines):
        for x, c in enumerate(v):
            p = Point(x, y)

            if c == '.':
                grid[p] = EMPTY
            elif c == '#':
                grid[p] = WALL
            else:
                grid[p] = 0
                fac = None
                loc = p
                if c == '^':
                    fac = N
                elif c == '>':
                    fac = E
                elif c == 'v':
                    fac = S
                elif c == '<':
                    fac = W
                guard_state = GuardState(loc, fac)
                guard_states.add(guard_state)

    guard_states, _ = patrol(grid, guard_state)
    result_a = len(set([s.loc for s in guard_states]))

    obs_locs_brute = set()
    pot_locs = set()
    obs_locs_smart = set()
    n = 0
    # for loc in grid:
    #     ### Try every grid location
    for loc in [s.loc for s in guard_states]:
        ### Try every grid location the guard initially went through
        n += 1
        if loc != guard_state.loc and grid[loc] == EMPTY:
            new_grid = grid.copy()
            new_grid[loc] = WALL

            _, escaped = patrol(new_grid, guard_state)
            if not escaped:
                obs_locs_brute.add(loc)

    #     ### Look if this completes a loop
    #     for f, v in VECTOR.items():
    #         pos = add_points(loc, v)
    #         if pos in grid and pos != guard_state.loc:
    #             # find if there's a loop from here
    #             test_guard = GuardState(pos, PREV[f])
    #             test_grid = grid.copy()
    #             test_grid[loc] = WALL
    #
    #             _, escaped = patrol(test_grid, test_guard)
    #             if not escaped:
    #                 pot_locs.add(loc)
    #
    # for loc in pot_locs:
    #     new_grid = grid.copy()
    #     new_grid[loc] = WALL
    #     _, escaped = patrol(new_grid, guard_state)
    #     if not escaped:
    #         obs_locs_smart.add(loc)

    print(f'Brute: {len(obs_locs_brute)}, Smart: {len(obs_locs_smart)}')

    result_b = len(obs_locs_brute)

    return result_a, result_b


def patrol(grid, guard_state):
    guard_states = {guard_state}
    while guard_state.loc in grid:
        loc, fac = guard_state
        next_loc = add_points(loc, VECTOR[fac])
        if next_loc not in grid:
            # Escaped
            break
        elif grid[next_loc] != WALL:
            loc = next_loc
        else:
            fac = NEXT[fac]

        guard_state = GuardState(loc, fac)
        if guard_state in guard_states:
            # Stuck
            return guard_states, False
        guard_states.add(guard_state)

    return guard_states, True
