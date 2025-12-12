import numpy as np


def solve_part_1(input_data):
    matrix = np.zeros((1000, 1000), dtype=np.int8)

    for line in input_data.strip().split("\n"):
        # Faster parsing using string operations
        if line.startswith('turn on'):
            coords = line[8:]  # Skip "turn on "
            state = 'on'
        elif line.startswith('turn off'):
            coords = line[9:]  # Skip "turn off "
            state = 'off'
        else:  # toggle
            coords = line[7:]  # Skip "toggle "
            state = 'toggle'

        # Parse coordinates more efficiently
        from_coor, to_coor = coords.split(' through ')
        from_x, from_y = map(int, from_coor.split(','))
        to_x, to_y = map(int, to_coor.split(','))

        # Use numpy slicing for vectorized operations
        region = matrix[from_y:to_y+1, from_x:to_x+1]
        if state == 'toggle':
            matrix[from_y:to_y+1, from_x:to_x+1] = 1 - region
        elif state == 'off':
            matrix[from_y:to_y+1, from_x:to_x+1] = 0
        elif state == 'on':
            matrix[from_y:to_y+1, from_x:to_x+1] = 1

    return int(np.sum(matrix))


def solve_part_2(input_data):
    matrix = np.zeros((1000, 1000), dtype=np.int32)

    for line in input_data.strip().split("\n"):
        # Faster parsing using string operations
        if line.startswith('turn on'):
            coords = line[8:]  # Skip "turn on "
            state = 'on'
        elif line.startswith('turn off'):
            coords = line[9:]  # Skip "turn off "
            state = 'off'
        else:  # toggle
            coords = line[7:]  # Skip "toggle "
            state = 'toggle'

        # Parse coordinates more efficiently
        from_coor, to_coor = coords.split(' through ')
        from_x, from_y = map(int, from_coor.split(','))
        to_x, to_y = map(int, to_coor.split(','))

        # Use numpy slicing for vectorized operations
        if state == 'toggle':
            matrix[from_y:to_y+1, from_x:to_x+1] += 2
        elif state == 'off':
            matrix[from_y:to_y+1, from_x:to_x+1] = np.maximum(0, matrix[from_y:to_y+1, from_x:to_x+1] - 1)
        elif state == 'on':
            matrix[from_y:to_y+1, from_x:to_x+1] += 1

    return int(np.sum(matrix))
