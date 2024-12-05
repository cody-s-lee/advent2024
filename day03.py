import re

from utils import with_content


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
