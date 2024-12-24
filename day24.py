import itertools
from collections import defaultdict

from utils import is_example, with_content


@with_content
def day24(content):
    result_b = 0

    values, gates = parse(content)

    values = execute(values, gates)
    result_a = extract(values, 'z')

    if is_example():
        assert result_a == 4
    else:
        assert result_a == 54715147844840

    # find 4 pairs of gates to swap
    # swap them, execute
    # if answer yields x + y == z good
    x, y, z = (extract(values, v) for v in 'xyz')
    print(f'{x} + {y} = {x + y} =? {z}')

    # find all pairs of gates
    gate_pairs = itertools.permutations(gates.keys(), 2)
    groups = itertools.permutations(gate_pairs, 4)

    potential_groups = []
    i = 0
    for group in groups:
        i += 1
        print(f'\rProcessing {i}/5,793,324,824,960,810,280', end='')
        test_gates = gates.copy()
        (p0, p1), (q0, q1), (r0, r1), (s0, s1) = group
        test_gates[p0], test_gates[p1] = test_gates[p1], test_gates[p0]
        test_gates[q0], test_gates[q1] = test_gates[q1], test_gates[q0]
        test_gates[r0], test_gates[r1] = test_gates[r1], test_gates[r0]
        test_gates[s0], test_gates[s1] = test_gates[s1], test_gates[s0]

        if x + y == extract(execute(values, test_gates), 'z'):
            potential_groups.append(group)
    print(f'\rProcessing {i}/5,793,324,824,960,810,280')

    print(f'Potential groups: {len(potential_groups)} -> {potential_groups}')

    return result_a, result_b


def execute(values, gates):
    all_vars: set[str] = {k for k in gates.keys()}
    for _, a, b in gates.values():
        all_vars.add(a)
        all_vars.add(b)
    queue = list(all_vars)
    while queue:
        v = queue.pop(0)
        if v in values:
            continue

        op, a, b = gates[v]
        if a not in values or b not in values:
            queue.append(v)
            continue

        values[v] = op(values[a], values[b])
    return values


def extract(values, name):
    ex_values = defaultdict(int)
    max_ex = 0
    for v in values:
        if v.startswith(name):
            ex_values[v] = values[v]
            max_ex = max(max_ex, int(v[1:]))
    ex_string = ''.join(str(int(ex_values[f'{name}{i:02}'])) for i in reversed(range(max_ex + 1)))
    result = int(ex_string, 2)
    return result


def parse(content) -> tuple[dict[str, bool], dict[str, tuple[callable, str, str]]]:
    inputs, gate_desc = content.split('\n\n')

    values = {}
    gates = {}

    for input in inputs.splitlines():
        k, v_s = input.split(': ')
        v = bool(int(v_s))
        values[k] = v

    for gate in gate_desc.splitlines():
        a, op_s, b, _, out = gate.split(' ')

        match op_s:
            case 'AND':
                op = lambda x, y: x and y
            case 'OR':
                op = lambda x, y: x or y
            case 'XOR':
                op = lambda x, y: x != y
            case _:
                raise ValueError(f'Unknown operator {op_s}')

        gates[out] = (op, a, b)

    return values, gates
