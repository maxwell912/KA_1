from pythonds.basic.stack import Stack
from dataclasses import dataclass
from typing import List


class Node:
    def __init__(self, x: int, y: int, prev=None):
        self.x = x
        self.y = y
        self.prev_node = prev

    def __hash__(self):
        return self.x + self.y * 1013

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def to_str(self):
        return '{0} {1}'.format(self.y + 1, self.x + 1)


@dataclass()
class Field:
    field: List[List[int]]
    width: int
    height: int

    def is_clear(self, node: Node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height and self.field[node.y][node.x] == 0


def get_start_info(input_file: str):
    with open(input_file, 'r', newline='\n') as file:
        height = int(file.readline())
        width = int(file.readline())
        field = [list() for _ in range(height)]
        for i in range(height):
            for cell in file.readline():
                if cell.isdigit():
                    field[i].append(int(cell))

        start_str = file.readline().split('  ')
        start = Node(int(start_str[1]) - 1, int(start_str[0]) - 1)

        end_str = file.readline().split('  ')
        end = Node(int(end_str[1]) - 1, int(end_str[0]) - 1)
        return Field(field, width, height), start, end


def find_way(field: Field, start: Node, end: Node):
    nodes_to_visit = Stack()
    visited_nodes = set()
    nodes_to_visit.push(start)
    visited_nodes.add(start)
    current_node: Node = start
    while current_node != end and not nodes_to_visit.isEmpty():
        current_node = nodes_to_visit.pop()
        for direction in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            next_node = Node(current_node.x + direction[0], current_node.y + direction[1], current_node)
            if field.is_clear(next_node) and next_node not in visited_nodes:
                visited_nodes.add(next_node)
                nodes_to_visit.push(next_node)
                if next_node == end:
                    current_node = next_node
                    break

    if nodes_to_visit.isEmpty():
        yield 'N'
        return
    yield 'Y'
    way: List[str] = list()
    while current_node is not None:
        way.append(current_node.to_str())
        current_node = current_node.prev_node
    way.reverse()
    yield from way


if __name__ == '__main__':
    input_file = 'input.txt'
    output_file = 'output.txt'
    with open('output.txt', 'w', newline='\n') as file:
        file.write('\n'.join(find_way(*get_start_info(input_file))))
