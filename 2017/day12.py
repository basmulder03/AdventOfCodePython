from collections import defaultdict


def solve_part_1(input_data):
    """Count programs in group containing program 0."""
    lines = input_data.strip().split('\n')
    connections = defaultdict(list)

    for line in lines:
        parts = line.split(' <-> ')
        prog = int(parts[0])
        connected = [int(x) for x in parts[1].split(', ')]
        connections[prog] = connected

    # BFS to find all connected to 0
    visited = set()
    queue = [0]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        queue.extend(connections[current])

    return len(visited)


def solve_part_2(input_data):
    """Count number of separate groups."""
    lines = input_data.strip().split('\n')
    connections = defaultdict(list)
    all_programs = set()

    for line in lines:
        parts = line.split(' <-> ')
        prog = int(parts[0])
        connected = [int(x) for x in parts[1].split(', ')]
        connections[prog] = connected
        all_programs.add(prog)

    visited_global = set()
    groups = 0

    for program in all_programs:
        if program in visited_global:
            continue

        # BFS for this group
        visited_local = set()
        queue = [program]

        while queue:
            current = queue.pop(0)
            if current in visited_local:
                continue
            visited_local.add(current)
            queue.extend(connections[current])

        visited_global.update(visited_local)
        groups += 1

    return groups
