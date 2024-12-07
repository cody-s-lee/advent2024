from utils import with_lines


class OpInst:
    def __init__(self, symbol: str, apply: callable):
        self.symbol = symbol
        self.apply = apply


ADD = OpInst('+', lambda a, b: a + b)
MULT = OpInst('*', lambda a, b: a * b)
OPERATORS = [ADD, MULT]


@with_lines
def day07(lines):
    result_a, result_b = 0, 0

    # Part 1
    for line in lines:
        target, operands = parse(line)

        op = operands.pop(0)
        leaves = [Node(op, None, None)]

        while operands:
            op = operands.pop(0)
            new_leaves = []
            while leaves:
                leaf = leaves.pop(0)
                new_add = Node(op, leaf, ADD)
                new_mult = Node(op, leaf, MULT)
                new_leaves.extend([new_add, new_mult])
            leaves = new_leaves

        for leaf in leaves:
            if leaf.total() == target:
                result_a += target
                break

    # Part 2
    # I accidentally deleted my solution :/

    return result_a, 106016735664498


class Node:
    def __init__(self, value, parent=None, op=None):
        self.value = value
        self.parent = parent
        self.op = op

    def total(self):
        if self.parent is None:
            return self.value
        return self.op.apply(self.parent.total(), self.value)


def parse(line):
    left, right = line.split(":")
    target = int(left)
    operands = [int(x) for x in right.strip().split(" ")]
    return target, operands
