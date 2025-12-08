from typing import Any
import math


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def get_component_sizes(self):
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = 0
            components[root] += 1
        return list(components.values())


def solve_part_1(input_data: str) -> Any:
    """Solve part 1 of the challenge."""
    lines = input_data.strip().split('\n')

    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    n = len(boxes)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)

    for idx, (dist, i, j) in enumerate(distances):
        if idx >= 1000:
            break
        uf.union(i, j)

    circuit_sizes = uf.get_component_sizes()
    circuit_sizes.sort(reverse=True)

    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result


def solve_part_2(input_data: str) -> Any:
    """Solve part 2 of the challenge."""
    lines = input_data.strip().split('\n')

    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    n = len(boxes)

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            distances.append((dist, i, j))

    distances.sort()

    uf = UnionFind(n)

    for dist, i, j in distances:
        if uf.union(i, j):
            num_circuits = len(set(uf.find(k) for k in range(n)))
            if num_circuits == 1:
                x1, y1, z1 = boxes[i]
                x2, y2, z2 = boxes[j]
                return x1 * x2

    return None
