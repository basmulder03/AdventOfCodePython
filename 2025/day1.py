def solve_part_1(input_data):
    p = 50
    zeros = 0

    for r in input_data.strip().split("\n"):
        if r[0] == 'R':
            p = (p + int(r[1:])) % 100
        elif r[0] == 'L':
            p = (p - int(r[1:])) % 100

        if p == 0:
            zeros += 1
    return zeros


def solve_part_2(input_data):
    p = 50
    zeros = 0

    for r in input_data.strip().split("\n"):
        amt = int(r[1:])

        if r[0] == 'R':
            dist = (100 - p) % 100
            if dist == 0: dist = 100

            if amt >= dist:
                zeros += 1 + (amt - dist) // 100
            p = (p + amt) % 100

        elif r[0] == 'L':
            dist = p if p != 0 else 100

            if amt >= dist:
                zeros += 1 + (amt - dist) // 100
            p = (p - amt) % 100

    return zeros

