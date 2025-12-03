from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    rs = []
    for l in ls:
        a, b = map(int, l.split('-'))
        rs.append((a, b))
    rs.sort()
    m = 0
    for a, b in rs:
        if a > m:
            return m
        m = max(m, b + 1)
    return m


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    rs = []
    for l in ls:
        a, b = map(int, l.split('-'))
        rs.append((a, b))
    rs.sort()
    mr = []
    for a, b in rs:
        if mr and a <= mr[-1][1] + 1:
            mr[-1] = (mr[-1][0], max(mr[-1][1], b))
        else:
            mr.append((a, b))
    c = 0
    for i in range(len(mr) - 1):
        c += mr[i+1][0] - mr[i][1] - 1
    c += mr[0][0]
    c += 4294967295 - mr[-1][1]
    return c

