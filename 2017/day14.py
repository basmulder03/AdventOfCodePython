def knot_hash(key):
    """Helper function to compute knot hash."""
    lengths = [ord(c) for c in key] + [17, 31, 73, 47, 23]
    rope = list(range(256))
    pos = 0
    skip = 0

    # 64 rounds
    for _ in range(64):
        for length in lengths:
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

    return ''.join(f'{x:02x}' for x in dense_hash)


def solve_part_1(input_data):
    """Count used squares in defrag grid."""
    key = input_data.strip()
    used_count = 0

    for i in range(128):
        row_key = f"{key}-{i}"
        hash_hex = knot_hash(row_key)

        # Convert hex to binary and count 1s
        for hex_char in hash_hex:
            binary = format(int(hex_char, 16), '04b')
            used_count += binary.count('1')

    return used_count


def solve_part_2(input_data):
    """Count connected regions in defrag grid."""
    key = input_data.strip()

    # Build the grid
    grid = []
    for i in range(128):
        row_key = f"{key}-{i}"
        hash_hex = knot_hash(row_key)
        row = []
        for hex_char in hash_hex:
            binary = format(int(hex_char, 16), '04b')
            row.extend([int(b) for b in binary])
        grid.append(row)

    visited = [[False] * 128 for _ in range(128)]
    regions = 0

    def dfs(r, c):
        if (r < 0 or r >= 128 or c < 0 or c >= 128 or
            visited[r][c] or grid[r][c] == 0):
            return

        visited[r][c] = True
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(128):
        for c in range(128):
            if grid[r][c] == 1 and not visited[r][c]:
                dfs(r, c)
                regions += 1

    return regions

