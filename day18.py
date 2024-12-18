from sortedcontainers import SortedList

from utils import CARDINAL_DIRECTIONS, Point, is_example, with_lines


def find_shortest_path_length(width, height, start, exit, corruption):
    def neighbors(point, corruption=corruption):
        for d in CARDINAL_DIRECTIONS:
            neighbor = point + d
            if 0 <= neighbor.x < width and 0 <= neighbor.y < height and neighbor not in corruption:
                yield neighbor

    distances = {start: 0}
    priority_queue = SortedList([start], key=lambda x: distances.get(x))
    visited = set()

    while priority_queue:
        current_point = priority_queue.pop(0)
        current_distance = distances[current_point]

        if current_point in visited:
            continue

        visited.add(current_point)

        if current_point == exit:
            return current_distance

        for neighbor in neighbors(current_point):
            if neighbor in corruption or neighbor in visited:
                continue

            new_distance = current_distance + 1
            if new_distance < distances.get(neighbor, 10 ** 9):
                distances[neighbor] = new_distance
                priority_queue.add(neighbor)

    return 10 ** 9


@with_lines
def day18(lines):
    start = Point(0, 0)
    if is_example():
        width, height = 7, 7
        exit = Point(6, 6)
    else:
        width, height = 71, 71
        exit = Point(70, 70)

    corruption = parse(lines)
    part_one_corruption = corruption[:12 if is_example() else 1024]

    result_a = find_shortest_path_length(width, height, start, exit, part_one_corruption)
    max_safe_index = find_max_safe_corruption_index(width, height, start, exit, corruption)

    return result_a, f'{corruption[max_safe_index].x},{corruption[max_safe_index].y}'


def find_max_safe_corruption_index(width, height, start, exit, corruption):
    low, high = 0, len(corruption)
    while low < high:
        mid = (low + high) // 2
        path_len = find_shortest_path_length(width, height, start, exit, corruption[:mid])
        if path_len == 10 ** 9:
            high = mid
        else:
            low = mid + 1
    return low - 1


def parse(lines):
    corruption = []
    for line in lines:
        x, y = map(int, line.split(','))
        corruption.append((Point(x, y)))

    return corruption
