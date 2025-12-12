from typing import Any


def solve_part_1(input_data: str) -> Any:
    lines = input_data.strip().split('\n')

    shape_sizes = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line and 'x' in line and ':' in line:
            break

        if line and line.endswith(':') and line[:-1].isdigit():
            shape_id = int(line[:-1])
            i += 1

            shape_size = 0
            while i < len(lines) and lines[i].strip() and 'x' not in lines[i]:
                shape_size += lines[i].count('#')
                i += 1

            shape_sizes[shape_id] = shape_size
        else:
            i += 1

    shape_sizes_list = [shape_sizes.get(j, 0) for j in range(6)]

    part1 = 0

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue

        colon_pos = line.find(':')
        if colon_pos == -1:
            continue

        dimensions = line[:colon_pos]
        x_pos = dimensions.find('x')
        if x_pos == -1:
            continue

        width = int(dimensions[:x_pos])
        height = int(dimensions[x_pos + 1:])
        grid_size = width * height

        quantities_str = line[colon_pos + 1:].strip()
        if not quantities_str:
            continue

        quantities = [int(x) for x in quantities_str.split()]

        total_area = sum(qty * shape_sizes_list[j] for j, qty in enumerate(quantities) if j < len(shape_sizes_list))

        if total_area <= grid_size:
            part1 += 1

    return part1


def solve_part_2(input_data: str) -> Any:
    return "Merry Christmas!"
