import re

def parse_reindeer(line):
    match = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.', line)
    if match:
        name, speed, fly_time, rest_time = match.groups()
        return {
            'name': name,
            'speed': int(speed),
            'fly_time': int(fly_time),
            'rest_time': int(rest_time)
        }
    return None

def calculate_distance(reindeer, total_time):
    cycle_time = reindeer['fly_time'] + reindeer['rest_time']
    complete_cycles = total_time // cycle_time
    remaining_time = total_time % cycle_time

    # Distance from complete cycles
    distance = complete_cycles * reindeer['speed'] * reindeer['fly_time']

    # Distance from remaining partial cycle
    if remaining_time > 0:
        fly_time_in_partial = min(remaining_time, reindeer['fly_time'])
        distance += fly_time_in_partial * reindeer['speed']

    return distance

def is_flying(reindeer, time):
    cycle_time = reindeer['fly_time'] + reindeer['rest_time']
    time_in_cycle = ((time - 1) % cycle_time) + 1
    return time_in_cycle <= reindeer['fly_time']

def solve_part_1(input_data):
    lines = input_data.strip().split('\n')
    reindeer_list = [parse_reindeer(line) for line in lines if line.strip()]
    reindeer_list = [r for r in reindeer_list if r is not None]

    race_time = 2503
    max_distance = 0

    for reindeer in reindeer_list:
        distance = calculate_distance(reindeer, race_time)
        max_distance = max(max_distance, distance)

    return max_distance

def solve_part_2(input_data):
    lines = input_data.strip().split('\n')
    reindeer_list = [parse_reindeer(line) for line in lines if line.strip()]
    reindeer_list = [r for r in reindeer_list if r is not None]

    race_time = 2503
    points = {reindeer['name']: 0 for reindeer in reindeer_list}

    # Simulate each second
    for second in range(1, race_time + 1):
        # Calculate current distances for all reindeer
        distances = {}
        for reindeer in reindeer_list:
            distances[reindeer['name']] = calculate_distance(reindeer, second)

        # Find the maximum distance at this second
        max_distance = max(distances.values())

        # Award points to all reindeer tied for the lead
        for name, distance in distances.items():
            if distance == max_distance:
                points[name] += 1

    return max(points.values())
