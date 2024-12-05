import itertools
import re
from collections import defaultdict
from operator import countOf

from args import get_args


def main():
    args = get_args()

    # Validation
    if args.day not in funcs:
        print(f"Day {args.day} not implemented")
        return

    # Prepare
    func = funcs[args.day]
    filename = f'day{args.day:02d}{"example" if args.example else ""}.txt'
    expected_a, expected_b = ((args.answers if args.answers else []) + [0, 0])[0:2]

    # Execute
    with open(filename, 'r') as file:
        result_a, result_b = func(file.read())
        print(f'Results: {result_a}, {result_b}')
        if expected_a or expected_b:
            print(f'Expected: {expected_a}, {expected_b}')


def with_lines(func):
    def wrapper(contents):
        return func(contents.split("\n"))

    return wrapper


def with_content(func):
    def wrapper(contents):
        return func(contents)

    return wrapper


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


@with_content
def day03(content):
    corrupted_program = content
    print(corrupted_program)

    result_a = 0
    result_b = 0

    matches = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', corrupted_program)
    for match in matches:
        print(match)
        x, y = [int(i) for i in match[4:-1].split(",")]
        result_a += x * y

    dos = corrupted_program.split(r'do()')
    for todo in dos:
        todo = todo.split(r"don't()")[0]
        matches = re.findall(r'mul\(\d\d?\d?,\d\d?\d?\)', todo)
        for match in matches:
            print(match)
            x, y = [int(i) for i in match[4:-1].split(",")]
            result_b += x * y

    return result_a, result_b


@with_lines
def day04(lines):
    result_a, result_b = 0, 0

    # Horizontal -
    print('Horizontal')
    for line in lines:
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
    for i, line in enumerate(lines):
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
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            diags[i + j] += c

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
    for i, line in enumerate(lines):
        for j, c in enumerate(line[::-1]):
            sgiad[i + j] += c

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

    num_lines = len(lines)
    len_lines = len(lines[0])

    for i in range(num_lines):
        for j in range(len_lines):
            if lines[i][j] == 'A':
                print(f'Considering A at {i}, {j}')

                # Skip edges
                if i == 0 or j == 0 or i == num_lines - 1 or j == len_lines - 1:
                    print(f'That A is on the edge')
                    continue

                x = lines[i - 1][j - 1] + lines[i + 1][j - 1] + lines[i + 1][j + 1] + lines[i - 1][j + 1]

                print(f'Surrounding letters are {x}')
                if (x == 'MMSS' or
                        x == 'MSSM' or
                        x == 'SSMM' or
                        x == 'SMMS'):
                    print(f'Found X-MAS at {i}, {j}')
                    result_b += 1

    return result_a, result_b


class Page:
    def __init__(self, id: int, children: set):
        self._id = id
        self._children = children

    @property
    def id(self):
        return self._id

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.add(child)


@with_content
def day05(content):
    result_a = 0
    result_b = 0

    rules, updates = (p.rstrip(' \n') for p in content.split('\n\n', maxsplit=1))

    print(f'Rules:\n{rules}')
    print('---------------')
    print(f'Updates:\n{updates}')
    print('---------------')

    # Create page index
    index = dict()
    for rule in sorted(rules.split('\n')):
        if not rule:
            continue

        print(f'Processing rule: {rule}')
        id, to = [int(p) for p in rule.split('|', maxsplit=1)]

        if id not in index:
            index[id] = Page(id, set())
        if to not in index:
            index[to] = Page(to, set())

        index[id].add_child(index[to])

    # Process updates
    incorrect_page_numbers_list = []
    for update in updates.split('\n'):
        if not update:
            continue

        print(f'Processing update: {update}')
        page_numbers = [int(p) for p in update.split(',')]

        # if the length of the pages is even, it's invalid
        if len(page_numbers) % 2 == 0:
            print(f'Invalid pages: {page_numbers}')
            raise ValueError('Invalid pages')

        # For each pair of pages with each later page, check if there is a counter-rule
        counter, _, _ = find_counter_example(index, page_numbers)
        if counter:
            print(f'Counter-rule found for {update}')
            incorrect_page_numbers_list.append(page_numbers)
        else:
            print(f'No counter-rule found for {update}')
            result_a += page_numbers[len(page_numbers) // 2]

    # PART 2
    # For each list of page numbers in incorrect_page_numbers_list
    for page_numbers in incorrect_page_numbers_list:
        print(f'Fixing page numbers: {page_numbers}')

        n = 0
        max_tries = len(page_numbers) * len(page_numbers)
        counter, i, j = find_counter_example(index, page_numbers)
        while counter and n < max_tries:
            page_numbers[j], page_numbers[i] = page_numbers[i], page_numbers[j]

            counter, i, j = find_counter_example(index, page_numbers)
            n += 1

        print(f'Corrected page numbers: {page_numbers} after {n} tries')

        result_b += page_numbers[len(page_numbers) // 2]

    return result_a, result_b


def find_counter_example(index, page_numbers):
    index = create_filtered_index(page_numbers, index)
    # index_str = {k: [c.id for c in v.children] for k, v in index.items()}
    # print(f'Using index {index_str} to fix {page_numbers}')
    for i, earlier in enumerate(page_numbers[:-1]):
        for j, later in enumerate(page_numbers[i + 1:]):
            queue = [(later, [later])]
            visited = set()
            while queue:
                current, current_path = queue.pop(0)
                visited.add(current)

                if current == earlier:
                    return current_path, i, i + j + 1

                for child in index[current].children:
                    if child.id not in visited and child.id in page_numbers:
                        queue.append((child.id, current_path + [child.id]))
    return None, None, None


def create_filtered_index(page_numbers, original_index):
    filtered_index = {}
    for page_number in page_numbers:
        if page_number in original_index:
            filtered_index[page_number] = Page(page_number, set())
            for child in original_index[page_number].children:
                if child.id in page_numbers:
                    if child.id not in filtered_index:
                        filtered_index[child.id] = Page(child.id, set())
                    filtered_index[page_number].add_child(filtered_index[child.id])
    return filtered_index


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
    5: day05,
}

if __name__ == '__main__':
    main()
