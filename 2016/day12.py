from typing import Any


def run(ls, r):
    i = 0
    while i < len(ls):
        p = ls[i].split()
        if p[0] == 'cpy':
            v = r[p[1]] if p[1] in r else int(p[1])
            r[p[2]] = v
        elif p[0] == 'inc':
            r[p[1]] += 1
        elif p[0] == 'dec':
            r[p[1]] -= 1
        elif p[0] == 'jnz':
            v = r[p[1]] if p[1] in r else int(p[1])
            if v != 0:
                i += int(p[2])
                continue
        i += 1
    return r['a']


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    r = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    return run(ls, r)


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    r = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    return run(ls, r)

