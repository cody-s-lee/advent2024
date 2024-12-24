import itertools
from collections import defaultdict

from utils import is_example, with_lines


@with_lines
def day23(lines):
    nodes, edges, neighbors, triples = parse(lines)

    if is_example():
        assert len(nodes) == 16
        assert len(edges) == 32
        assert len(triples) == 12

    result_a = sum(1 for a, b, c in triples if a.startswith('t') or b.startswith('t') or c.startswith('t'))

    if is_example():
        assert result_a == 7
    else:
        assert result_a == 1411

    cliques = list(bron_kerbosch(set(), nodes, set(), neighbors))
    party = max(cliques, key=len)

    result_b = ','.join(sorted(party))

    if is_example():
        assert result_b == 'co,de,ka,ta'
    else:
        assert result_b == 'aq,bn,ch,dt,gu,ow,pk,qy,tv,us,yx,zg,zu'

    return result_a, result_b


def bron_kerbosch(r: set[str], p: set[str], x: set[str], neighbors: dict[str, set[str]]) -> set[str]:
    if not p and not x:
        yield r
    while p:
        v = p.pop()
        yield from bron_kerbosch(
            r.union({v}),
            p.intersection(neighbors[v]),
            x.intersection(neighbors[v]),
            neighbors
        )
        x.add(v)


def parse(lines):
    edges = {buple(*l.split('-')) for l in lines}
    neighbors = defaultdict(set)
    for e in edges:
        a, b = e
        neighbors[a].add(b)
        neighbors[b].add(a)
    nodes = {k for k in neighbors.keys()}
    triples = set()
    for a, ns in neighbors.items():
        for b, c in itertools.combinations(ns, 2):
            if buple(b, c) not in edges:
                continue
            triples.add(tuple(sorted([a, b, c])))
    return nodes, edges, neighbors, triples


class buple:
    _m = None
    _n = None

    def __init__(self, *args):
        self._m, self._n = sorted(args[:2])

    def __str__(self):
        return f'{self._m}-{self._n}'

    def __repr__(self):
        return f'buple({self._m!r}, {self._n!r})'

    def __lt__(self, other):
        return self._m < other._m or (self._m == other._m and self._n < other._n)

    def __eq__(self, other):
        return self._m == other._m and self._n == other._n

    def __gt__(self, other):
        return self._m > other._m or (self._m == other._m and self._n > other._n)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return 2

    def __hash__(self):
        return hash((self._m, self._n))

    def __iter__(self):
        return iter((self._m, self._n))

    def __getitem__(self, i):
        if i == 0:
            return self._m
        elif i == 1:
            return self._n
        else:
            raise AttributeError


def test_buple_builtins():
    a = buple('kh', 'ti')
    b = buple('ti', 'kh')
    assert a == b
    assert hash(a) == hash(b)
    assert not (a < b)
    assert not (b > a)
    assert a <= b
    assert b >= a
    assert not (a != b)
    assert a[0] == 'kh'
    assert b[0] == 'kh'
    assert a[1] == 'ti'
    assert b[1] == 'ti'
    assert list(a) == ['kh', 'ti']
    assert list(b) == ['kh', 'ti']
    try:
        _ = a[2]
        assert False
    except AttributeError:
        pass
    try:
        a[0] = 2
        assert False
    except TypeError:
        pass
    try:
        _ = a.m
        assert False
    except AttributeError:
        pass
    try:
        a.n
        assert False
    except AttributeError:
        pass
