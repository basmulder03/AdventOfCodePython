def solve_part_1(input_data):
    """Electromagnetic moat - find strongest bridge."""
    lines = input_data.strip().split('\n')
    components = []

    for line in lines:
        a, b = map(int, line.split('/'))
        components.append((a, b))

    def dfs(port, used, strength):
        max_strength = strength

        for i, (a, b) in enumerate(components):
            if i in used:
                continue

            if a == port:
                new_used = used | {i}
                max_strength = max(max_strength, dfs(b, new_used, strength + a + b))
            elif b == port:
                new_used = used | {i}
                max_strength = max(max_strength, dfs(a, new_used, strength + a + b))

        return max_strength

    return dfs(0, set(), 0)


def solve_part_2(input_data):
    """Electromagnetic moat - find strongest bridge among longest."""
    lines = input_data.strip().split('\n')
    components = []

    for line in lines:
        a, b = map(int, line.split('/'))
        components.append((a, b))

    def dfs(port, used, strength, length):
        results = [(length, strength)]

        for i, (a, b) in enumerate(components):
            if i in used:
                continue

            if a == port:
                new_used = used | {i}
                results.extend(dfs(b, new_used, strength + a + b, length + 1))
            elif b == port:
                new_used = used | {i}
                results.extend(dfs(a, new_used, strength + a + b, length + 1))

        return results

    all_bridges = dfs(0, set(), 0, 0)

    # Find maximum length
    max_length = max(length for length, strength in all_bridges)

    # Among bridges of maximum length, find maximum strength
    max_strength = max(strength for length, strength in all_bridges if length == max_length)

    return max_strength

