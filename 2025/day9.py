from typing import Any
from itertools import combinations, pairwise

def solve_part_1(input_data: str) -> Any:
    points = []
    for line in input_data.strip().split('\n'):
        points.append(eval(line))

    max_area = 0

    for (x1, y1), (x2, y2) in combinations(points, 2):
        min_x, max_x = sorted((x1, x2))
        min_y, max_y = sorted((y1, y2))

        rectangle_area = (max_x - min_x + 1) * (max_y - min_y + 1)
        max_area = max(max_area, rectangle_area)

    return max_area


def solve_part_2(input_data: str) -> Any:
    points = []
    for line in input_data.strip().split('\n'):
        points.append(eval(line))

    max_valid_area = 0

    for (x1, y1), (x2, y2) in combinations(points, 2):
        min_x, max_x = sorted((x1, x2))
        min_y, max_y = sorted((y1, y2))

        rectangle_area = (max_x - min_x + 1) * (max_y - min_y + 1)

        for (edge_x1, edge_y1), (edge_x2, edge_y2) in pairwise(points + [points[0]]):
            edge_min_x, edge_max_x = sorted((edge_x1, edge_x2))
            edge_min_y, edge_max_y = sorted((edge_y1, edge_y2))
            if all((min_x < edge_max_x, max_x > edge_min_x, min_y < edge_max_y, max_y > edge_min_y)):
                break
        else:
            max_valid_area = max(max_valid_area, rectangle_area)

    return max_valid_area
