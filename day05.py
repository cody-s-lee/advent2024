from functools import cmp_to_key

from utils import with_content


class Page:
    def __init__(self, id_: int, children: set):
        self._id = id_
        self._children = children

    @property
    def id(self):
        return self._id

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.add(child)


def cmp_pages(a, b):
    if a not in b.children and b not in a.children:
        return 0

    if a in b.children:
        return 1

    if b in a.children:
        return -1

    raise RuntimeError('Should not reach here')


@with_content
def day05(content):
    result_a = 0
    result_b = 0

    rules, updates = (p.rstrip(' \n') for p in content.split('\n\n', maxsplit=1))

    print(f'Rules:\n{rules}')
    print('---------------')
    print(f'Updates:\n{updates}')
    print('---------------')

    # Create page index
    index = dict()
    for rule in sorted(rules.split('\n')):
        if not rule:
            continue

        print(f'Processing rule: {rule}')
        id_, to = [int(p) for p in rule.split('|', maxsplit=1)]

        if id_ not in index:
            index[id_] = Page(id_, set())
        if to not in index:
            index[to] = Page(to, set())

        index[id_].add_child(index[to])

    # Process updates
    incorrect_page_numbers_list = []
    for update in updates.split('\n'):
        if not update:
            continue

        print(f'Processing update: {update}')
        page_numbers = [int(p) for p in update.split(',')]

        # if the length of the pages is even, it's invalid
        if len(page_numbers) % 2 == 0:
            print(f'Invalid pages: {page_numbers}')
            raise ValueError('Invalid pages')

        # For each pair of pages with each later page, check if there is a counter-rule
        counter, _, _ = find_counter_example(index, page_numbers)
        if counter:
            print(f'Counter-rule found for {page_numbers}')
            pages = [index[p] for p in page_numbers]
            print(f'Pages: {pages}')
            print(f'Sorted: {sorted(pages, key=cmp_to_key(cmp_pages))}')
            incorrect_page_numbers_list.append(page_numbers)
        else:
            print(f'No counter-rule found for {page_numbers}')
            result_a += page_numbers[len(page_numbers) // 2]

    # PART 2
    # For each list of page numbers in incorrect_page_numbers_list
    for page_numbers in incorrect_page_numbers_list:
        original_page_numbers = page_numbers.copy()
        print(f'Fixing page numbers: {page_numbers}')

        pages = [index[p] for p in page_numbers]
        sorted_page_numbers = [p.id for p in sorted(pages, key=cmp_to_key(cmp_pages))]
        print(f'Maybe could be sorted as: {sorted_page_numbers}')
        result_b += sorted_page_numbers[len(page_numbers) // 2]

    return result_a, result_b


def find_counter_example(index, page_numbers):
    index = create_filtered_index(page_numbers, index)
    for i, earlier in enumerate(page_numbers[:-1]):
        for j, later in enumerate(page_numbers[i + 1:]):
            queue = [(later, [later])]
            visited = set()
            while queue:
                current, current_path = queue.pop(0)
                visited.add(current)

                if current == earlier:
                    return current_path, i, i + j + 1

                for child in index[current].children:
                    if child.id not in visited and child.id in page_numbers:
                        queue.append((child.id, current_path + [child.id]))
    return None, None, None


def create_filtered_index(page_numbers, original_index):
    filtered_index = {}
    for page_number in page_numbers:
        if page_number in original_index:
            filtered_index[page_number] = Page(page_number, set())
            for child in original_index[page_number].children:
                if child.id in page_numbers:
                    if child.id not in filtered_index:
                        filtered_index[child.id] = Page(child.id, set())
                    filtered_index[page_number].add_child(filtered_index[child.id])
    return filtered_index
