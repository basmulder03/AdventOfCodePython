def solve_part_1(input_data):
    """Dancing programs - perform dance moves."""
    programs = list("abcdefghijklmnop")
    moves = input_data.strip().split(',')

    for move in moves:
        if move[0] == 's':  # Spin
            size = int(move[1:])
            programs = programs[-size:] + programs[:-size]
        elif move[0] == 'x':  # Exchange positions
            a, b = map(int, move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif move[0] == 'p':  # Partner (exchange by name)
            a, b = move[1:].split('/')
            idx_a = programs.index(a)
            idx_b = programs.index(b)
            programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

    return ''.join(programs)


def solve_part_2(input_data):
    """Dance programs 1 billion times - find cycle."""
    programs = list("abcdefghijklmnop")
    moves = input_data.strip().split(',')

    seen = {}
    cycle = 0

    while True:
        state = ''.join(programs)
        if state in seen:
            cycle_start = seen[state]
            cycle_length = cycle - cycle_start
            remaining = (1_000_000_000 - cycle_start) % cycle_length

            # Run remaining iterations
            for _ in range(remaining):
                for move in moves:
                    if move[0] == 's':
                        size = int(move[1:])
                        programs = programs[-size:] + programs[:-size]
                    elif move[0] == 'x':
                        a, b = map(int, move[1:].split('/'))
                        programs[a], programs[b] = programs[b], programs[a]
                    elif move[0] == 'p':
                        a, b = move[1:].split('/')
                        idx_a = programs.index(a)
                        idx_b = programs.index(b)
                        programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

            return ''.join(programs)

        seen[state] = cycle

        # Perform one iteration
        for move in moves:
            if move[0] == 's':
                size = int(move[1:])
                programs = programs[-size:] + programs[:-size]
            elif move[0] == 'x':
                a, b = map(int, move[1:].split('/'))
                programs[a], programs[b] = programs[b], programs[a]
            elif move[0] == 'p':
                a, b = move[1:].split('/')
                idx_a = programs.index(a)
                idx_b = programs.index(b)
                programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

        cycle += 1

