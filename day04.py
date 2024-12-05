import re
from collections import defaultdict

from utils import with_lines


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
