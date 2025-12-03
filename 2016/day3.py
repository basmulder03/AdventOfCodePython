from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    c = 0
    for l in ls:
        n = [int(x) for x in l.split()]
        if n[0] + n[1] > n[2] and n[0] + n[2] > n[1] and n[1] + n[2] > n[0]:
            c += 1
    return c


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    ns = [[int(x) for x in l.split()] for l in ls]
    c = 0
    for i in range(0, len(ns), 3):
        for j in range(3):
            a, b, d = ns[i][j], ns[i+1][j], ns[i+2][j]
            if a + b > d and a + d > b and b + d > a:
                c += 1
    return c

