def solve_part_1(input_data):
    """Spiral Memory - Manhattan distance from center."""
    target = int(input_data.strip())

    if target == 1:
        return 0

    # Find which layer the target is in
    layer = 0
    while (2 * layer + 1) ** 2 < target:
        layer += 1

    # Size of the current layer
    layer_size = 2 * layer + 1
    max_in_layer = layer_size ** 2

    # Find position within the layer
    position_in_layer = target - (layer_size - 2) ** 2

    # Each side has layer_size elements, find which side
    side_length = layer_size - 1
    side = (position_in_layer - 1) // side_length
    pos_in_side = (position_in_layer - 1) % side_length

    # Distance from middle of side
    middle_offset = abs(pos_in_side - layer + 1)

    return layer + middle_offset


def solve_part_2(input_data):
    """Spiral Memory - First value larger than input."""
    target = int(input_data.strip())

    if target == 1:
        return 2

    # Build spiral with sum of adjacent values
    grid = {(0, 0): 1}
    x, y = 0, 0
    dx, dy = 1, 0  # Start moving right

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, up, left, down
    dir_idx = 0
    steps = 1
    step_count = 0

    while True:
        # Move in current direction
        x += dx
        y += dy

        # Calculate sum of adjacent values
        value = sum(grid.get((x+i, y+j), 0)
                   for i in [-1, 0, 1] for j in [-1, 0, 1])

        if value > target:
            return value

        grid[(x, y)] = value
        step_count += 1

        # Change direction if needed
        if step_count == steps:
            step_count = 0
            dir_idx = (dir_idx + 1) % 4
            dx, dy = directions[dir_idx]

            # Increase step count after every 2 direction changes
            if dir_idx % 2 == 0:
                steps += 1

