from day01 import day01
from day02 import day02
from day03 import day03
from day04 import day04
from day05 import day05
from day06 import day06
from day07 import day07
from day08 import day08
from day09 import day09
from day10 import day10
from day11 import day11
from day12 import day12
from day13 import day13
from day14 import day14
from day15 import day15
from day16 import day16
from day17 import day17
from day18 import day18
from day19 import day19
from day20 import day20
from utils import get_args


def main():
    args = get_args()
    days = args.day if not args.all else funcs.keys()

    if not days:
        print("No days selected")

    results = dict()
    for day in sorted(days):
        # Validation
        if day not in funcs:
            print(f"Day {day} not implemented")
            return

        # Prepare
        func = funcs[day]
        filename = f'day{day:02d}{"example" if args.example else ""}.txt'

        # Execute
        with open(filename, 'r') as file:
            result_a, result_b = func(file.read())
            results[day] = (result_a, result_b)
            print(f'Results: {result_a}, {result_b}')

    for day in sorted(days):
        print(f'Day {day} results: {results[day]}')


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
    6: day06,
    7: day07,
    8: day08,
    9: day09,
    10: day10,
    11: day11,
    12: day12,
    13: day13,
    14: day14,
    15: day15,
    16: day16,
    17: day17,
    18: day18,
    19: day19,
    20: day20,
}

if __name__ == '__main__':
    main()
