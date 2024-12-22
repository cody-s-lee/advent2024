import itertools
from functools import cache, lru_cache
from multiprocessing import Manager, Pool

from utils import with_lines


def sx(i):
    lock.acquire()
    lock.value += 1
    print(f'\rIn progress: {doing.value}, completed: {done.value}/{len(secrets)}        ', end='')
    lock.release()

    secquences[i] = secquence_2k(secrets[i])

    lock.acquire()
    doing.value -= 1
    done.value += 1
    print(f'\rIn progress: {doing.value}, completed: {done.value}/{len(secrets)}        ', end='')
    lock.release()


def ix(i):
    secq = secquences[i]
    _insets = insets_x(secq)
    for inset, value in _insets:
        inset_maps[(i, inset)] = value


def insets_x(secq: list[int]) -> list[tuple[tuple[int, ...], int]]:  # start pos, inset tuple, end value
    results = []

    deltas = [(j % 10) - (i % 10) for i, j in itertools.pairwise(secq)]
    for start in range(len(deltas) - 4):
        results.append((tuple(deltas[start:start + 4]), secq[start + 4] % 10))

    return results


def init_pool_processes(the_lock, the_doing, the_done, the_secquences, the_secrets, the_inset_maps, the_all_insets):
    global lock
    lock = the_lock

    global doing
    doing = the_doing

    global done
    done = the_done

    global secquences
    secquences = the_secquences

    global secrets
    secrets = the_secrets

    global inset_maps
    inset_maps = the_inset_maps

    global all_insets
    all_insets = the_all_insets


@with_lines
def day22(lines):
    num_lines = len(lines)

    manager = Manager()
    _init_secrets = manager.dict({i: int(l) for i, l in enumerate(lines)})
    _lock = manager.Lock(),
    _doing = manager.Value('i', 0),
    _done = manager.Value('i', 0),
    _secquences = manager.dict(),
    _secrets = _init_secrets,
    _inset_maps = manager.dict(),
    _all_insets = manager.list(),
    pool = Pool(processes=64, initializer=init_pool_processes,
                initargs=(_lock, _doing, _done, _secquences, _secrets, _inset_maps, _all_insets,))

    print(f'Processing secquences:')
    pool.imap_unordered(sx, range(num_lines))
    print(f'\rIn progress: {_doing.value}, completed: {_done.value}/{len(secrets)}        ')

    result_a = sum(s[2000] for s in _secquences.values())

    print(f'Processing insets:')
    pool.imap_unordered(ix, range(num_lines))

    print(f'Processing all_insets:')
    _all_insets.extend(ins for ins in {inset for _, inset in _inset_maps.keys()})

    print(f'Processing profits:')
    profits = [pft for pft in pool.imap_unordered(pfx, all_insets)]
    max_profit = max(profits)

    # 2445

    return result_a, max_profit


def pfx(inset):
    pft = 0
    for i in range(len(secrets)):
        pft + inset_maps.get((i, inset), 0)
    return pft


def profit_for_secquences(ins, secquences) -> int:
    return sum(profit(secq, ins) for secq in secquences)


@cache
def secret(x, n=1):
    for _ in range(n):
        x = _secret(x)

    return x


def secquence(x: int, n: int) -> list[int]:
    return [secret(x, i) for i in range(0, n + 1)]


def secquence_2k(x: int) -> list[int]:
    # print(f'Calculating secquence for {x}')
    result = secquence(x, 2000)
    # print(f'Finished calculating secquence for {x}')
    return result


def profit(secq: list[int] | tuple[int], inseq: list[int] | tuple[int, int, int, int]) -> int:
    return _profit(tuple(secq), tuple(inseq))


@lru_cache
def _profit(secq: tuple[int], inseq: tuple[int, int, int, int]) -> int:
    deltas = [(j % 10) - (i % 10) for i, j in itertools.pairwise(secq)]

    for i in range(0, len(deltas) - 4):
        if tuple(deltas[i:i + 4]) == inseq:
            return secq[i + 4] % 10

    return 0


def insets(secq: list[int]) -> set[tuple[int, int, int, int]]:
    deltas = [(j % 10) - (i % 10) for i, j in itertools.pairwise(secq)]
    return set((deltas[i], deltas[i + 1], deltas[i + 2], deltas[i + 3]) for i in range(len(deltas) - 4))


@cache
def _secret(x):
    x ^= (x << 6)
    x %= (2 ** 24)
    x ^= (x >> 5)
    x %= (2 ** 24)
    x ^= (x << 11)
    x %= (2 ** 24)
    return x


def test_secret():
    x = 123
    secrets = [secret(x, i) for i in range(1, 11)]
    assert secrets == [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]


def test_secquence():
    x = 123
    secrets = secquence(x, 10)
    assert secrets == [123, 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]


def test_profit():
    x = 2024
    secq = secquence(x, 2000)

    assert profit(secq, [-2, 1, -1, 3]) == 9

    pass


def test_part2():
    initial_secrets = [1, 2, 3, 2024]

    pool = Pool(20)
    secquences = pool.map(secquence_2k, initial_secrets)

    all_ins = {ins for secq in secquences for ins in insets(secq)}
    profits: dict[tuple, int] = dict()
    print(f'All ins: {len(all_ins)}')

    n = 0
    max_profit = 0
    for ins in all_ins:
        if n % 1000 == 0:
            print(f'Progress: {n}/{len(all_ins)}, max_profit: {max_profit}')
        n += 1

        profits[ins] = sum(profit(secq, ins) for secq in secquences)
        max_profit = max(max_profit, profits[ins])

    assert max_profit == 23
