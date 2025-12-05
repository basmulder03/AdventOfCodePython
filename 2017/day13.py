def solve_part_1(input_data):
    """Packet scanners - calculate severity."""
    lines = input_data.strip().split('\n')
    scanners = {}

    for line in lines:
        depth, range_val = map(int, line.split(': '))
        scanners[depth] = range_val

    severity = 0
    for depth, range_val in scanners.items():
        # Scanner position at time t is: t % (2 * (range - 1))
        # At depth, time is depth, so position is depth % (2 * (range - 1))
        if depth % (2 * (range_val - 1)) == 0:
            severity += depth * range_val

    return severity


def solve_part_2(input_data):
    """Find delay to pass through without being caught."""
    lines = input_data.strip().split('\n')
    scanners = {}

    for line in lines:
        depth, range_val = map(int, line.split(': '))
        scanners[depth] = range_val

    delay = 0
    while True:
        caught = False
        for depth, range_val in scanners.items():
            # With delay, we arrive at depth at time (delay + depth)
            if (delay + depth) % (2 * (range_val - 1)) == 0:
                caught = True
                break

        if not caught:
            return delay

        delay += 1
