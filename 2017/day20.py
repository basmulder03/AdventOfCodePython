def solve_part_1(input_data):
    """Particle swarm - find particle closest to origin long term."""
    lines = input_data.strip().split('\n')
    particles = []

    for i, line in enumerate(lines):
        parts = line.split(', ')
        pos = list(map(int, parts[0][3:-1].split(',')))
        vel = list(map(int, parts[1][3:-1].split(',')))
        acc = list(map(int, parts[2][3:-1].split(',')))
        particles.append((pos, vel, acc, i))

    # Particle with smallest Manhattan acceleration will be closest long-term
    min_acc = float('inf')
    result = 0

    for pos, vel, acc, idx in particles:
        manhattan_acc = sum(abs(a) for a in acc)
        if manhattan_acc < min_acc:
            min_acc = manhattan_acc
            result = idx
        elif manhattan_acc == min_acc:
            # If acceleration is same, check velocity
            manhattan_vel = sum(abs(v) for v in vel)
            current_best = particles[result]
            best_manhattan_vel = sum(abs(v) for v in current_best[1])
            if manhattan_vel < best_manhattan_vel:
                result = idx

    return result


def solve_part_2(input_data):
    """Particle swarm - count remaining particles after collisions."""
    lines = input_data.strip().split('\n')
    particles = {}

    for i, line in enumerate(lines):
        parts = line.split(', ')
        pos = list(map(int, parts[0][3:-1].split(',')))
        vel = list(map(int, parts[1][3:-1].split(',')))
        acc = list(map(int, parts[2][3:-1].split(',')))
        particles[i] = (pos, vel, acc)

    # Simulate for enough time for collisions to settle
    for tick in range(1000):
        # Update positions and velocities
        for i in list(particles.keys()):
            if i in particles:
                pos, vel, acc = particles[i]
                # Update velocity
                vel = [vel[j] + acc[j] for j in range(3)]
                # Update position
                pos = [pos[j] + vel[j] for j in range(3)]
                particles[i] = (pos, vel, acc)

        # Check for collisions
        positions = {}
        for i, (pos, vel, acc) in particles.items():
            pos_tuple = tuple(pos)
            if pos_tuple not in positions:
                positions[pos_tuple] = []
            positions[pos_tuple].append(i)

        # Remove collided particles
        for pos, particle_list in positions.items():
            if len(particle_list) > 1:
                for particle_id in particle_list:
                    if particle_id in particles:
                        del particles[particle_id]

    return len(particles)

