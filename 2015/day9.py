from itertools import permutations

def parse_input(input_data):
    """Parse the input to create a distance dictionary and set of cities."""
    distances = {}
    cities = set()

    for line in input_data.strip().split('\n'):
        parts = line.split(' = ')
        route = parts[0]
        distance = int(parts[1])

        city1, city2 = route.split(' to ')
        cities.add(city1)
        cities.add(city2)

        # Store distances in both directions
        distances[(city1, city2)] = distance
        distances[(city2, city1)] = distance

    return distances, cities

def calculate_route_distance(route, distances):
    """Calculate the total distance for a given route."""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[(route[i], route[i + 1])]
    return total_distance

def solve_part_1(input_data):
    """Find the shortest route that visits all cities exactly once."""
    distances, cities = parse_input(input_data)

    min_distance = float('inf')

    # Try all possible permutations of cities
    for route in permutations(cities):
        distance = calculate_route_distance(route, distances)
        min_distance = min(min_distance, distance)

    return min_distance

def solve_part_2(input_data):
    """Find the longest route that visits all cities exactly once."""
    distances, cities = parse_input(input_data)

    max_distance = 0

    # Try all possible permutations of cities
    for route in permutations(cities):
        distance = calculate_route_distance(route, distances)
        max_distance = max(max_distance, distance)

    return max_distance
