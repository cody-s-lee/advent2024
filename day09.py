from utils import with_content


@with_content
def day09(content):
    filesystem = parse(content)
    print(filesystem)

    filesystem = compress1(filesystem)
    result_a = checksum(filesystem)
    print(f'{''.join([str(i) for i in filesystem])}: {result_a}')

    raw = parseraw(content)
    filesystem = compressraw2filesystem(raw)
    result_b = checksum(filesystem)
    print(f'{''.join([str(i) if i != -1 else '-' for i in filesystem])}: {result_b}')

    return result_a, result_b


def parseraw(content) -> list[int]:
    return [int(i) for i in content]


def parse(content):
    filesystem = []
    file_index = 0

    for i in range(0, len(content), 2):
        # Add file blocks
        f = int(content[i])

        for j in range(f):
            filesystem.append(file_index)
        file_index += 1

        # Add empty space
        if i + 1 >= len(content):
            break

        e = int(content[i + 1])

        for j in range(e):
            filesystem.append(-1)

    return filesystem


def used(filesystem):
    return sum(1 for file_index in filesystem if file_index != -1)


def squish(filesystem):
    return [file_index for file_index in filesystem if file_index != -1]


def compress1(filesystem):
    compressed = []
    size = used(filesystem)

    squished = squish(reversed(filesystem))

    squindex = 0
    for i in range(size):
        match filesystem[i]:
            case -1:
                compressed.append(squished[squindex])
                squindex += 1
            case x:
                compressed.append(x)

    return compressed


def compressraw2filesystem(raw: list[int]):
    # raw is of the format list[int]
    # where the value is the file or empty size
    raw = cleanup(raw)

    files, empties = raw2dicts(raw)

    # for each file, starting from the last
    for filename in reversed(files.keys()):
        file_index, file_size = files[filename]

        # for each empty space
        for empty_index in sorted(empties.keys()):
            empty_size = empties[empty_index]

            # if the empty is to the left of the file
            if empty_index >= file_index:
                continue

            # if the empty size is at least as large as the file size
            if empty_size >= file_size:
                # move the file to the empty space
                new_file_index = empty_index
                files[filename] = (new_file_index, file_size)

                # make the empty smaller and advance its index
                new_empty_size = empty_size - file_size
                new_empty_index = empty_index + file_size
                del empties[empty_index]
                empties[new_empty_index] = new_empty_size

                break

    return dicts2filesystem(files, empties)


def dicts2filesystem(files: dict[int, tuple[int, int]], empties: dict[int, int]):
    # find len of the filesystem by finding the max index+size of files and empties
    filesystem_len = 0
    for idx, size in files.values():
        filesystem_len = max(filesystem_len, idx + size)
    for idx, size in empties.items():
        filesystem_len = max(filesystem_len, idx + size)

    filesystem = [-1] * filesystem_len

    for filename, (idx, size) in files.items():
        for i in range(size):
            filesystem[idx + i] = filename

    return filesystem


def combine(empty: list[tuple[int, int]]) -> list[tuple[int, int]]:
    empty = sorted(empty)
    combined = []

    done = False
    while not done:
        done = True

        # look for adjacent empty spaces
        for i, e in enumerate(empty):
            for j, f in enumerate(empty):
                if i == j:
                    continue

                if e[0] + e[1] == f[0]:
                    empty[i] = (e[0], e[1] + f[1])
                    del empty[j]
                    done = False
                    break

    return combined


def raw2dicts(raw: list[int]):
    files: dict[int, tuple[int, int]] = dict()  # filename:(index, size)
    empties: dict[int, int] = dict()  # index: size

    raw = cleanup(raw)

    filename = 0
    index = 0
    for i in range(0, len(raw), 2):
        file_size = raw[i]
        files[filename] = (index, file_size)
        filename += 1
        index += file_size

        empty_size = raw[i + 1]
        if empty_size > 0:
            empties[index] = empty_size
        index += empty_size

    return files, empties


def cleanup(raw):
    cleaned = raw[:]
    if len(raw) % 2 != 0:
        cleaned.append(0)
    return cleaned


def compress2(filesystem):
    compressed = []

    empty_spaces = []  # list of tuple (index, size)
    for i, f in enumerate(filesystem):
        if f != -1:
            continue

        if f == -1:
            j = i + 1
            for j in range(i + 1, len(filesystem)):
                if filesystem[j] != -1:
                    break

            empty_spaces.append((i, j - i))

    rev = list(reversed(filesystem))

    for i, fi in enumerate(rev):
        # skip past empty space
        if fi == -1:
            continue

    return compressed


def checksum(filesystem):
    cs = 0
    for i, f in enumerate(filesystem):
        if f != -1:
            cs += (i * f)

    return cs
