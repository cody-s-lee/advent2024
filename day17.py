from utils import with_content


@with_content
def day17(content):
    a, b, c, pgm = parse(content)
    _, _, _, out = execute(pgm, a, b, c)
    out = xlate(a, b, c)

    result_a = ','.join(str(x) for x in out)

    # Part 2

    result_b = a

    return result_a, result_b


def xlate(a, b, c):
    out = []

    # do {
    done = False
    while not done:
        # 2,4, -> bst (4->a)
        b = a % 8

        # 1,5, -> bxl (5)
        b = b ^ 5

        # 7,5, -> cdv (5->b)
        c = a >> b

        # 4,3, -> bxc (3->x)
        b = b ^ c

        # 1,6, -> bxl (6)
        b = b ^ 6

        # 0,3, -> adv (3)
        a = a >> 3

        # 5,5, -> out (5->b)
        out.append(b % 8)

        # 3,0 -> jnz (0)
        # } while a != 0
        done = (a == 0)

    return out


def execute(pgm, a, b, c):
    pc = 0
    out = []
    while pc < len(pgm) - 1:
        op, x = pgm[pc], pgm[pc + 1]
        pc += 2
        match op:
            case 0:
                a = a >> dc(x, a, b, c)  # adv
            case 1:
                b = b ^ x  # bxl
            case 2:
                b = dc(x, a, b, c) % 8  # bst
            case 3:
                if a != 0:  # jnz
                    pc = x
            case 4:
                b = b ^ c  # bxc
            case 5:
                out.append(dc(x, a, b, c) % 8)  # out
            case 6:
                b = a >> dc(x, a, b, c)  # bdv
            case 7:
                c = a >> dc(x, a, b, c)  # cdv

    return a, b, c, out


def dc(operand, a, b, c):
    match operand:
        case operand if operand <= 3:
            return operand
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c


def parse(content):
    a, b, c, program = 0, 0, 0, []

    for line in content.splitlines():
        if line.startswith("Register A"):
            a = int(line.split(" ")[-1])
        elif line.startswith("Register B"):
            b = int(line.split(" ")[-1])
        elif line.startswith("Register C"):
            c = int(line.split(" ")[-1])
        elif line.startswith("Program"):
            instructions = line.split(" ")[-1]
            program = [int(i) for i in instructions.split(",")]

    return a, b, c, program


if __name__ == "__main__":
    with open('day17example.txt', 'r') as file:
        result_a, result_b = day17(file.read())
        print(f'Results: {result_a}, {result_b}')
