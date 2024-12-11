import re
from collections import defaultdict

from utils import with_content

Z = re.compile(r'\b(0)\b')
E = re.compile(r'\b((?:\d\d)+)\b')
O = re.compile(r'\b([1-9](?:\d\d)*)\b')
C = re.compile(r'x')


def evenrepl(match):
    s = match.group(1)
    m, n = s[:len(s) // 2], s[len(s) // 2:].lstrip('0')
    m = '0' if not m else m
    n = '0' if not n else n
    return f'x{m}  x{n}'


@with_content
def day11re(content):
    content = content.replace(' ', '  ')

    # 123456 385 0

    # apply evens rule
    # x123 x456 385 0

    # apply odds rule
    # x123 x456 385*2024 0

    # apply zeros rule
    # x123 x456 385*2024 1

    # commit evens rule             # apply simultaneously
    # 123 456 385*2024 1            # 123 456 385*2024 1

    for _ in range(25):
        print(f'[{_}] {len(content)}')

        # apply evens rule
        content = E.sub(evenrepl, content)

        # apply odds rule
        for match in reversed(list(O.finditer(content))):
            # print(match)
            content = content[:match.start(1)] + str(2024 * int(match.group(1))) + content[match.end(1):]
        pass

        # apply zeros rule
        content = Z.sub(' 1 ', content)

        # commit evens rule
        content = C.sub('', content)

    result_a = len(content.split('  '))

    for _ in range(50):
        print(f'[{_ + 25}] {len(content)}')

        # apply evens rule
        content = E.sub(evenrepl, content)

        # apply odds rule
        for match in reversed(list(O.finditer(content))):
            # print(match)
            content = content[:match.start(1)] + str(2024 * int(match.group(1))) + content[match.end(1):]
        pass

        # apply zeros rule
        content = Z.sub(' 1 ', content)

        # commit evens rule
        content = C.sub('', content)

    result_b = len(content.split('  '))

    return result_a, result_b


@with_content
def day11dict(content):
    stones = parsedict(content)

    for _ in range(25):
        updates: dict[int, int] = defaultdict(int)
        for stone, count in stones.items():
            if stone == 0:
                updates[1] += count
            else:
                s = str(stone)
                if len(s) % 2 == 0:
                    updates[int(s[:len(s) // 2])] += count
                    updates[int(s[len(s) // 2:])] += count
                else:
                    updates[stone * 2024] += count

        stones = updates
    result_a = sum(c for c in stones.values())

    for _ in range(50):
        updates: dict[int, int] = defaultdict(int)
        for stone, count in stones.items():
            if stone == 0:
                updates[1] += count
            else:
                s = str(stone)
                if len(s) % 2 == 0:
                    updates[int(s[:len(s) // 2])] += count
                    updates[int(s[len(s) // 2:])] += count
                else:
                    updates[stone * 2024] += count

        stones = updates
    result_b = sum(c for c in stones.values())

    return result_a, result_b


def parsedict(content) -> dict[int, int]:
    return {int(x): 1 for x in content.split(" ")}


@with_content
def day11ll(content):
    l = [int(x) for x in content.split(' ')]

    result_a = sum(len(expand(x, 25)) for x in l)
    result_b = sum(len(expand(x, 75)) for x in l)

    return result_a, result_b


def parse(content):
    l = [int(x) for x in content.split(" ")]

    head = Node(l.pop(0), None)
    curr = head
    while l:
        curr.n = Node(l.pop(0), None)
        curr = curr.n

    return head


class Node:
    def __init__(self, x, n):
        self.x = x
        self.n = n

    def __str__(self):
        s = f'({self.x})'
        node = self.n
        while node:
            s += f' ({node.x})'
            node = node.n
        return s

    @staticmethod
    def size(node):
        n = 0
        while node:
            n += 1
            node = node.n
        return n

    @staticmethod
    def str(node):
        s = str(node.x)
        node = node.n
        while node:
            s += " " + str(node.x)
            node = node.n

        return s


EXPANSIONS: dict[tuple[int, int], list[int]] = {}


# memoize expansions
def expand(x: int, n: int) -> list:
    if (x, n) in EXPANSIONS:
        return EXPANSIONS[(x, n)]

    l = [x]

    for i in range(n):
        if (x, i) in EXPANSIONS:
            l = EXPANSIONS[(x, i)]
            continue

        m = []
        for z in l:
            if z == 0:
                m.append(1)
            elif len(str(z)) % 2 == 0:
                s = str(z)
                m.extend([int(s[:len(s) // 2]), int(s[len(s) // 2:])])
            else:
                m.append(z * 2024)
        l = m
        EXPANSIONS[(x, i)] = l

    return l


day11 = day11dict
