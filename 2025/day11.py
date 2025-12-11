from typing import Any
from functools import reduce
from operator import mul


def solve_part_1(input_data: str) -> Any:
    graph = {line.split(': ')[0]: line.split(': ')[1].split()
             for line in input_data.strip().split('\n') if ':' in line}

    if 'out' not in graph:
        graph['out'] = []

    def count_paths(current: str, target: str, visited: set, memo: dict) -> int:
        if current == target:
            return 1

        memo_key = (current, target)
        if memo_key in memo:
            return memo[memo_key]

        if current in visited or current not in graph:
            return 0

        visited.add(current)
        total = sum(count_paths(neighbor, target, visited, memo)
                   for neighbor in graph[current])
        visited.remove(current)

        memo[memo_key] = total
        return total

    return count_paths('you', 'out', set(), {}) if 'you' in graph else 0


def solve_part_2(input_data: str) -> Any:
    graph = {line.split(': ')[0]: line.split(': ')[1].split()
             for line in input_data.strip().split('\n') if ':' in line}

    if 'out' not in graph:
        graph['out'] = []

    required = ['svr', 'dac', 'fft', 'out']
    if not all(device in graph for device in required):
        return 0

    def count_paths(start: str, end: str) -> int:
        def dfs(current: str, target: str, visited: set, memo: dict) -> int:
            if current == target:
                return 1

            memo_key = (current, target)
            if memo_key in memo:
                return memo[memo_key]

            if current in visited or current not in graph:
                return 0

            visited.add(current)
            total = sum(dfs(neighbor, target, visited, memo)
                       for neighbor in graph[current])
            visited.remove(current)

            memo[memo_key] = total
            return total

        return dfs(start, end, set(), {})

    path_segments = [
        [('svr', 'dac'), ('dac', 'fft'), ('fft', 'out')],
        [('svr', 'fft'), ('fft', 'dac'), ('dac', 'out')]
    ]

    return sum(reduce(mul, (count_paths(start, end) for start, end in segments), 1)
               for segments in path_segments)
