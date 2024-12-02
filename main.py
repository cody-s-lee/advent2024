import argparse
import itertools
from operator import countOf


def example():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    args = parser.parse_args()

    # Validation
    if args.day not in funcs:
        print(f"Day {args.day} not implemented")
        return

    # Prepare
    func = funcs[args.day]
    input_url = f'https://adventofcode.com/2024/day/{args.day}/input'

    # Execute
    with open(f'day{args.day:02d}.txt', 'r') as file:
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
}

if __name__ == '__main__':
    example()
