def solve_part_1(input_data):
    """Count lengths after 40 iterations of knot hash."""
    lengths = [int(x) for x in input_data.strip().split(',')]
    rope = list(range(256))
    pos = 0
    skip = 0

    for length in lengths:
        # Reverse the portion of the rope
        if length > 1:
            indices = [(pos + i) % 256 for i in range(length)]
            values = [rope[i] for i in indices]
            values.reverse()
            for i, val in zip(indices, values):
                rope[i] = val

        pos = (pos + length + skip) % 256
        skip += 1

    return rope[0] * rope[1]


def solve_part_2(input_data):
    """Generate full knot hash."""
    key = input_data.strip()
    lengths = [ord(c) for c in key] + [17, 31, 73, 47, 23]
    rope = list(range(256))
    pos = 0
    skip = 0

    # 64 rounds
    for _ in range(64):
        for length in lengths:
            # Reverse the portion of the rope
            if length > 1:
                indices = [(pos + i) % 256 for i in range(length)]
                values = [rope[i] for i in indices]
                values.reverse()
                for i, val in zip(indices, values):
                    rope[i] = val

            pos = (pos + length + skip) % 256
            skip += 1

    # Create dense hash
    dense_hash = []
    for i in range(16):
        block = rope[i*16:(i+1)*16]
        xor_result = block[0]
        for j in range(1, 16):
            xor_result ^= block[j]
        dense_hash.append(xor_result)

    # Convert to hex
    return ''.join(f'{x:02x}' for x in dense_hash)
