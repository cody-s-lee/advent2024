import itertools

from utils import with_lines


def pairwise(iterable):
    """s -> (s0, s1), (s1, s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


@with_lines
def day02(lines):
    result_a = 0
    for i, line in enumerate(lines):
        if len(line) == 0:
            continue

        print(f'{i}: {line}: ', end='')

        levels = [int(l) for l in line.split(" ")]

        direction = 0
        for (x, y) in pairwise(levels):
            if abs(x - y) < 1 or abs(x - y) > 3:
                print('unsafe')
                break  # unsafe

            if direction == 0:
                direction = 1 if x < y else -1

            if x < y and direction == -1:
                print('unsafe')
                break  # unsafe
            if x > y and direction == 1:
                print('unsafe')
                break  # unsafe
        else:
            # safe
            print('safe')
            result_a += 1

    result_b = 0
    for i, line in enumerate(lines):
        if len(line) == 0:
            continue

        print(f'{i}: {line}: ', end='')

        levels = [int(l) for l in line.split(" ")]

        is_safe = False

        direction = 0
        for (x, y) in pairwise(levels):
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

        if not is_safe:
            for j in range(len(levels)):
                sub_levels = levels[:j] + levels[j + 1:]
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
