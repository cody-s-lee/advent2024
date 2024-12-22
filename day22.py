import itertools
from functools import cache, lru_cache, partial
from multiprocessing import Manager, Pool

from utils import with_lines

global num_lines
global lock
global doing
global done


def sx(args):
    i, x = args
    lock.acquire()
    doing.value += 1
    print(f'\rIn progress: {doing.value}, completed: {done.value}/{num_lines}        ', end='')
    lock.release()

    result = (i, sequence_2k(x))

    lock.acquire()
    doing.value -= 1
    done.value += 1
    print(f'\rIn progress: {doing.value}, completed: {done.value}/{num_lines}        ', end='')
    lock.release()

    return result


def ix(args: tuple[int, list[int]], num_sequences: int) -> list[tuple[tuple[int, tuple[int, ...]], int]]:
    i, seq = args
    
    _insets = insets(seq)  # sequence -> inset tuple, value
    results = []
    for inset, value in _insets:
        if (i, inset) not in results:
            results.append(((i, inset), value))

    lock.acquire()
    done.value += 1
    print(f'\rProcessed {done.value}/{num_sequences} entries', end='')
    lock.release()

    return results  # list[ ( (i,inset), value ) ]


def insets(seq: list[int]) -> list[tuple[tuple[int, ...], int]]:  # start pos, inset tuple, end value
    results = []

    deltas = [(j % 10) - (i % 10) for i, j in itertools.pairwise(seq)]
    insets_seen = set()
    for start in range(len(deltas) - 4):
        inset = tuple(deltas[start:start + 4])
        if inset in insets_seen:
            continue

        results.append((inset, seq[start + 4] % 10))
        insets_seen.add(inset)

    return results


def init_pool_processes(the_lock, the_doing, the_done, the_num_lines):
    global lock
    lock = the_lock

    global doing
    doing = the_doing

    global done
    done = the_done

    global num_lines
    num_lines = the_num_lines


@with_lines
def day22(lines):
    init_secrets = [(i, int(l)) for i, l in enumerate(lines)]
    num_lines = len(lines)

    manager = Manager()

    lock = manager.Lock()
    doing = manager.Value('i', 0)
    done = manager.Value('i', 0)

    pool = Pool(processes=64, initializer=init_pool_processes, initargs=(lock, doing, done, num_lines,))

    print(f'Processing sequences:')
    sequences = {k: v for k, v in pool.imap_unordered(sx, init_secrets)}
    print(f'\rIn progress: {doing.value}, completed: {done.value}/{num_lines}        ')

    result_a = sum(s[2000] for s in sequences.values())

    print(f'Processing insets...')
    done.value = 0
    inset_map_entry_lists = pool.imap_unordered(partial(ix, num_sequences=len(sequences)), sequences.items())
    inset_map = dict()
    for entry_list in inset_map_entry_lists:
        for key, value in entry_list:
            inset_map[key] = value
    print(f'\rProcessed {len(inset_map)}/{len(sequences)} entries')

    print(f'Processing all_insets:')
    all_insets = {ins for _, ins in inset_map.keys()}

    print(f'Processing profits:')
    inset_profit_map = dict()
    for inset in all_insets:
        # print(f'Processing inset: {inset}', end='')
        inset_profit = 0
        for i in range(num_lines):
            inset_profit += inset_map.get((i, inset), 0)
        inset_profit_map[inset] = inset_profit
        # print(f'\rProcessing inset: {inset} -> {inset_profit}')

    result_b = max(inset_profit_map.values())

    # 2445

    return result_a, result_b


@cache
def secret(x, n=1):
    for _ in range(n):
        x = _secret(x)

    return x


def sequence(x: int, n: int) -> list[int]:
    return [secret(x, i) for i in range(0, n + 1)]


def sequence_2k(x: int) -> list[int]:
    # print(f'Calculating sequence for {x}')
    result = sequence(x, 2000)
    # print(f'Finished calculating sequence for {x}')
    return result


def profit(seq: list[int] | tuple[int], inseq: list | tuple) -> int:
    return _profit(tuple(seq), tuple(inseq))


@lru_cache
def _profit(seq: tuple[int], inseq: tuple) -> int:
    deltas = [(j % 10) - (i % 10) for i, j in itertools.pairwise(seq)]

    for i in range(0, len(deltas) - 4):
        if tuple(deltas[i:i + 4]) == inseq:
            return seq[i + 4] % 10

    return 0


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


def test_sequence():
    x = 123
    secrets = sequence(x, 10)
    assert secrets == [123, 15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]


def test_profit():
    x = 2024
    seq = sequence(x, 2000)

    assert profit(seq, [-2, 1, -1, 3]) == 9

    pass


def test_part2():
    initial_secrets = [1, 2, 3, 2024]

    pool = Pool(20)
    sequences = pool.map(sequence_2k, initial_secrets)

    all_ins = {ins for seq in sequences for ins in insets(seq)}
    profits: dict[tuple, int] = dict()
    print(f'All ins: {len(all_ins)}')

    n = 0
    max_profit = 0
    for ins in all_ins:
        if n % 1000 == 0:
            print(f'Progress: {n}/{len(all_ins)}, max_profit: {max_profit}')
        n += 1

        profits[ins] = sum(profit(seq, ins) for seq in sequences)
        max_profit = max(max_profit, profits[ins])

    assert max_profit == 23
