import argparse
import urllib.request

import ssl


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

    # Create an SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Execute
    with urllib.request.urlopen(input_url, context=ssl_context) as response:
        print(do(response.read().decode('utf-8').split("\n"), func))


def day01(line):
    # Count number of unique letters in the line
    unique = set(line)

    return len(unique)


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
}

if __name__ == '__main__':
    example()
