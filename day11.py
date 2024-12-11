from utils import with_content


@with_content
def day11(content):
    hair = Node(0, parse(content))

    print(Node.str(hair.n))

    for _ in range(25):
        prev, curr = hair, hair.n
        while curr:

            if curr.x == 0:
                curr.x = 1
            elif len(str(curr.x)) % 2 == 0:
                s = str(curr.x)
                l, r = int(s[:len(s) // 2]), int(s[len(s) // 2:])

                p = Node(r, curr.n)
                o = Node(l, p)

                prev.n = o
                curr = p
            else:
                curr.x = curr.x * 2024

            prev, curr = curr, curr.n

        # sz = Node.size(hair.n)
        # st = Node.str(hair.n)
        # print(f'{_}: {sz}, {st}')

    result_a = Node.size(hair.n)

    for _ in range(50):
        prev, curr = hair, hair.n
        while curr:

            if curr.x == 0:
                curr.x = 1
            elif len(str(curr.x)) % 2 == 0:
                s = str(curr.x)
                l, r = int(s[:len(s) // 2]), int(s[len(s) // 2:])

                p = Node(r, curr.n)
                o = Node(l, p)

                prev.n = o
                curr = p
            else:
                curr.x = curr.x * 2024

            prev, curr = curr, curr.n

    result_b = Node.size(hair.n)

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
