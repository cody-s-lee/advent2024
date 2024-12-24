import re

import numpy as np

from point import Point
from utils import with_content

MACHINE_RE = re.compile(r'^Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)$',
                        re.MULTILINE)


@with_content
def day13(content):
    machines = parse(content)

    result_a = best_cost(machines)

    for machine in machines:
        machine.prize += Point(10000000000000, 10000000000000)

    result_b = best_cost(machines)

    return result_a, result_b


def best_cost(machines):
    total = 0
    for machine in machines:
        solution = machine.solve()

        if solution is not None:
            num_a, num_b = solution
            total += 3 * num_a + num_b
    return total


class Machine:
    def __init__(self, prize: Point, a: Point, b: Point):
        self.prize = prize
        self.a = a
        self.b = b

    def is_winner(self, num_a, num_b):
        return (self.a.mul_scalar(num_a) + self.b.mul_scalar(num_b)) == self.prize

    def solve(self):
        eq = np.array([[self.a.x, self.b.x], [self.a.y, self.b.y]])
        res = np.array([self.prize.x, self.prize.y])

        num_a, num_b = (int(round(x)) for x in np.linalg.solve(eq, res))
        if self.is_winner(num_a, num_b):
            return num_a, num_b

        return None


def parse(content) -> list[Machine]:
    machines = []
    for info in content.split('\n\n'):
        match = MACHINE_RE.match(info)
        assert match is not None

        machines.append(Machine(Point(int(match.group(5)), int(match.group(6))),
                                Point(int(match.group(1)), int(match.group(2))),
                                Point(int(match.group(3)), int(match.group(4)))))
    return machines
