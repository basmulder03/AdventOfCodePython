def solve_part_1(input_data):
    import math

    f = input_data.splitlines()
    times = [int(numbs) for numbs in f[0].split()[1::]]
    distances = [int(numbs) for numbs in f[1].split()[1::]]

    total = 1
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]

        # Same quadratic formula approach as part 2
        discriminant = time * time - 4 * distance
        if discriminant <= 0:
            continue

        sqrt_discriminant = math.sqrt(discriminant)
        root1 = (time - sqrt_discriminant) / 2
        root2 = (time + sqrt_discriminant) / 2

        # Integer values in the range (root1, root2) exclusive
        lower_bound = int(math.floor(root1 + 1e-9)) + 1 if root1 == int(root1) else int(math.ceil(root1))
        upper_bound = int(math.ceil(root2 - 1e-9)) - 1 if root2 == int(root2) else int(math.floor(root2))

        valid_methods = max(0, upper_bound - lower_bound + 1)
        total *= valid_methods

    return total

def solve_part_2(input_data):
    import math

    f = input_data.splitlines()
    time = int(''.join(f[0].split()[1::]))
    distance = int(''.join(f[1].split()[1::]))

    # We need to solve: push_time * (time - push_time) > distance
    # Rearranging: -push_time^2 + time*push_time - distance > 0
    # This is a quadratic: -x^2 + time*x - distance = 0
    # Using quadratic formula: x = (-b ± sqrt(b^2 - 4ac)) / 2a
    # Where a = -1, b = time, c = -distance

    discriminant = time * time - 4 * distance
    if discriminant <= 0:
        return 0

    sqrt_discriminant = math.sqrt(discriminant)

    # The two roots (bounds where the equation equals 0)
    root1 = (time - sqrt_discriminant) / 2
    root2 = (time + sqrt_discriminant) / 2

    # We need integer values that are strictly greater than distance
    # So we need the range (root1, root2) exclusive
    lower_bound = int(math.floor(root1 + 1e-9)) + 1 if root1 == int(root1) else int(math.ceil(root1))
    upper_bound = int(math.ceil(root2 - 1e-9)) - 1 if root2 == int(root2) else int(math.floor(root2))

    return max(0, upper_bound - lower_bound + 1)
