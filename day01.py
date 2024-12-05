from operator import countOf

from utils import with_lines


@with_lines
def day01(lines):
    result_a = 0
    lefts = []
    rights = []
    for i, line in enumerate(lines):
        if len(line) == 0:
            continue

        print(f'{i}: {line}')

        line = line.strip()
        left, right = line.split(" ", maxsplit=1)
        lefts.append(int(left))
        rights.append(int(right))

    lefts = sorted(lefts)
    rights = sorted(rights)

    assert len(lefts) == len(rights)

    for i in range(len(lefts)):
        l, r = lefts[i], rights[i]

        result_a += abs(l - r)

    result_b = 0

    for l in lefts:
        result_b += l * countOf(rights, l)

    return result_a, result_b
