from typing import Any


def solve_part_1(input_data: str) -> Any:
    data = list(input_data.strip())
    target_len = 272

    while len(data) < target_len:
        # Create inverted reverse: a becomes a + '0' + reverse(invert(a))
        b = ['0' if c == '1' else '1' for c in reversed(data)]
        data.extend(['0'] + b)

    # Trim to target length
    data = data[:target_len]

    # Calculate checksum
    while len(data) % 2 == 0:
        new_data = []
        for i in range(0, len(data), 2):
            new_data.append('1' if data[i] == data[i+1] else '0')
        data = new_data

    return ''.join(data)


def solve_part_2(input_data: str) -> Any:
    data = list(input_data.strip())
    target_len = 35651584

    while len(data) < target_len:
        # Create inverted reverse: a becomes a + '0' + reverse(invert(a))
        b = ['0' if c == '1' else '1' for c in reversed(data)]
        data.extend(['0'] + b)

    # Trim to target length
    data = data[:target_len]

    # Calculate checksum
    while len(data) % 2 == 0:
        new_data = []
        for i in range(0, len(data), 2):
            new_data.append('1' if data[i] == data[i+1] else '0')
        data = new_data

    return ''.join(data)

