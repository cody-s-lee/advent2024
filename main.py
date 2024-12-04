import argparse
import itertools
import re
from collections import defaultdict
from email.policy import default
from operator import countOf


def example():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("-x", "--example", action="store_true", help="Use example file")
    args = parser.parse_args()

    # Validation
    if args.day not in funcs:
        print(f"Day {args.day} not implemented")
        return

    # Prepare
    func = funcs[args.day]
    filename = f'day{args.day:02d}{"example" if args.example else ""}.txt'

    # Execute
    with open(filename, 'r') as file:
        print(func(file.read().split("\n")))



def day01(reader):
    result_a = 0
    lefts = []
    rights = []
    for i, line in enumerate(reader):
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

def pairwise(iterable):
    """s -> (s0, s1), (s1, s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def day02(reader):
    result_a = 0
    for i, line in enumerate(reader):
        if len(line) == 0:
            continue

        print(f'{i}: {line}: ', end='')

        levels = [int(l) for l in line.split(" ")]

        direction = 0
        for (x, y) in pairwise(levels):
            if abs(x - y) <1 or abs(x-y) > 3:
                print('unsafe')
                break # unsafe

            if direction == 0:
                direction = 1 if x < y else -1

            if x < y and direction == -1:
                print('unsafe')
                break #unsafe
            if x > y and direction == 1:
                print('unsafe')
                break #unsafe
        else:
            # safe
            print('safe')
            result_a += 1

    result_b = 0
    for i, line in enumerate(reader):
        if len(line) == 0:
            continue

        print(f'{i}: {line}: ', end='')

        levels = [int(l) for l in line.split(" ")]

        is_safe = False

        direction = 0
        for (x, y) in pairwise(levels):
            if abs(x - y) <1 or abs(x-y) > 3:
                break # unsafe

            if direction == 0:
                direction = 1 if x < y else -1

            if x < y and direction == -1:
                break #unsafe
            if x > y and direction == 1:
                break #unsafe
        else:
            # safe
            is_safe = True

        if not is_safe:
            for j in range(len(levels)):
                sub_levels = levels[:j] + levels[j+1:]
                direction = 0
                for (x, y) in pairwise(sub_levels):
                    if abs(x - y) < 1 or abs(x - y) > 3:
                        break  # unsafe

                    if direction == 0:
                        direction = 1 if x < y else -1

                    if x < y and direction == -1:
                        break  # unsafe
                    if x > y and direction == 1:
                        break  # unsafe
                else:
                    # safe
                    is_safe = True
                    break

        if is_safe:
            print('safe')
            result_b += 1
        else:
            print('unsafe')


    return result_a, result_b

def day03(reader):
    corrupted_program = ''.join(reader)
    print(corrupted_program)

    result_a = 0
    result_b = 0

    matches = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', corrupted_program)
    for match in matches:
        print(match)
        x, y = [int(i) for i in match[4:-1].split(",")]
        result_a += x*y

    dos = corrupted_program.split(r'do()')
    for todo in dos:
        todo = todo.split(r"don't()")[0]
        matches = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', todo)
        for match in matches:
            print(match)
            x, y = [int(i) for i in match[4:-1].split(",")]
            result_b += x * y

    return result_a, result_b

def day04(reader):
    result_a, result_b = 0, 0

    # Horizontal -
    print('Horizontal')
    for line in reader:
        print(f'Evaluating {line}')

        # Forward
        x = len(re.findall('XMAS', line))
        result_a += x

        # Backward
        y = len(re.findall('XMAS', line[::-1]))
        result_a += y

        print(f'Found {x} forward and {y} backward')

    # Vertical |
    print('Vertical')
    verts = []
    for i, line in enumerate(reader):
        for j, c in enumerate(line):
            if i == 0:
                verts.append(c)
            else:
                verts[j] += c
    for vert in verts:
        print(f'Evaluating {vert}')

        # Down
        x = len(re.findall('XMAS', vert))
        result_a += x

        # Up
        y = len(re.findall('XMAS', vert[::-1]))
        result_a += y

        print(f'Found {x} forward and {y} downward')

    # Diagonal \
    print('Diagonal \\')
    diags = defaultdict(str)
    for i, line in enumerate(reader):
        for j, c in enumerate(line):
            diags[i+j] += c

    for diag in diags.values():
        print(f'Evaluating {diag}')

        # / Down
        x = len(re.findall('XMAS', diag))
        result_a += x

        # / Up
        y = len(re.findall('XMAS', diag[::-1]))
        result_a += y

        print(f'Found {x} forward and {y} backward')

    # Diagonal /
    print('Diagonal /')
    sgiad = defaultdict(str)
    for i, line in enumerate(reader):
        for j, c in enumerate(line[::-1]):
            sgiad[i+j] += c

    for giad in sgiad.values():
        print(f'Evaluating {giad}')

        # \ Down
        x = len(re.findall('XMAS', giad))
        result_a += x

        # \ Up
        y = len(re.findall('XMAS', giad[::-1]))
        result_a += y

        print(f'Found {x} forward and {y} backward')

    # PART 2
    # X-MAS
    # For every A at i, j, look for M-M and S-S

    num_lines = len(reader)
    len_lines = len(reader[0])

    for i in range(num_lines):
        for j in range(len_lines):
            if reader[i][j] == 'A':
                print(f'Considering A at {i}, {j}')

                # Skip edges
                if i == 0 or j == 0 or i == num_lines-1 or j == len_lines-1:
                    print(f'That A is on the edge')
                    continue

                x = reader[i-1][j-1] + reader[i+1][j-1] + reader[i+1][j+1] + reader[i-1][j+1]

                print(f'Surrounding letters are {x}')
                if (x == 'MMSS' or
                        x == 'MSSM' or
                        x == 'SSMM' or
                        x == 'SMMS'):
                    print(f'Found X-MAS at {i}, {j}')
                    result_b += 1

    return result_a, result_b



def do(reader, processor):
    result = 0
    for i, line in enumerate(reader):
        line = line.strip()
        if len(line) == 0:
            continue
        print(f'{i}: {line}')
        result += processor(line)
    return result

funcs = {
    1: day01,
    2: day02,
    3: day03,
    4: day04,
}

if __name__ == '__main__':
    example()
