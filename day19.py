from functools import cache

from utils import with_content


@with_content
def day19(content):
    towels, patterns = parse(content)

    result_a = count_valid(towels, patterns)
    result_b = count_arrangements(towels, patterns)

    return result_a, result_b


def parse(content) -> tuple[tuple, list[str]]:
    towel_line, pattern_lines = content.split('\n\n')
    towels: tuple = tuple({str(t.strip()) for t in towel_line.split(',')})
    patterns: list[str] = pattern_lines.split('\n')

    return towels, patterns


def count_valid(towels, patterns) -> int:
    return sum(1 if valid(towels, pattern) else 0 for pattern in patterns)


@cache
def valid(towels, pattern) -> bool:
    # valid returns true if the set of towels can be combined into the pattern string
    # so if the set of towels is {rg, uw, br} then the pattern "rgbw" is invalid but "rgbruw" is valid

    # if the pattern is empty, then we're good
    if not pattern:
        return True

    # if any of the towels prefix the pattern then we're good if the rest of the pattern is valid
    for towel in towels:
        if pattern.startswith(towel):
            if valid(towels, pattern[len(towel):]):
                return True

    return False


def count_arrangements(towels, patterns) -> int:
    return sum(num_arrangements(towels, pattern) for pattern in patterns)


@cache
def num_arrangements(towels, pattern) -> int:
    # num_arrangements returns the number of ways that the pattern can be constructed by the given towels

    # if the pattern is empty, then we're good
    if not pattern:
        return 1

    # if any of the towels prefix the pattern then we're good if the rest of the pattern is valid
    return sum(
        num_arrangements(towels, pattern[len(towel):])
        for towel in towels if pattern.startswith(towel)
    )


if __name__ == "__main__":
    with open('day19example.txt', 'r') as file:
        result_a, result_b = day19(file.read())
        print(f'Results: {result_a}, {result_b}')
