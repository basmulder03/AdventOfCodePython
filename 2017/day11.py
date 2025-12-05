def solve_part_1(input_data):
    """Find distance after hexagonal grid walk."""
    directions = input_data.strip().split(',')

    # Hexagonal coordinates: q, r, s (where q + r + s = 0)
    q, r, s = 0, 0, 0

    for direction in directions:
        if direction == 'n':
            r -= 1
            s += 1
        elif direction == 's':
            r += 1
            s -= 1
        elif direction == 'ne':
            q += 1
            r -= 1
        elif direction == 'sw':
            q -= 1
            r += 1
        elif direction == 'nw':
            q -= 1
            s += 1
        elif direction == 'se':
            q += 1
            s -= 1

    # Distance in cube coordinates is (|q| + |r| + |s|) / 2
    return (abs(q) + abs(r) + abs(s)) // 2


def solve_part_2(input_data):
    """Find maximum distance during hexagonal walk."""
    directions = input_data.strip().split(',')

    q, r, s = 0, 0, 0
    max_distance = 0

    for direction in directions:
        if direction == 'n':
            r -= 1
            s += 1
        elif direction == 's':
            r += 1
            s -= 1
        elif direction == 'ne':
            q += 1
            r -= 1
        elif direction == 'sw':
            q -= 1
            r += 1
        elif direction == 'nw':
            q -= 1
            s += 1
        elif direction == 'se':
            q += 1
            s -= 1

        # Calculate current distance
        distance = (abs(q) + abs(r) + abs(s)) // 2
        max_distance = max(max_distance, distance)

    return max_distance
