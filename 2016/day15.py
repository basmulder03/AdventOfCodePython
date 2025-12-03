from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    ds = []
    for l in ls:
        p = l.split()
        n = int(p[3])
        pos = int(p[-1][:-1])
        ds.append((n, pos))
    t = 0
    while True:
        ok = True
        for i, (n, pos) in enumerate(ds):
            if (pos + t + i + 1) % n != 0:
                ok = False
                break
        if ok:
            return t
        t += 1


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    ds = []
    for l in ls:
        p = l.split()
        n = int(p[3])
        pos = int(p[-1][:-1])
        ds.append((n, pos))
    ds.append((11, 0))
    t = 0
    while True:
        ok = True
        for i, (n, pos) in enumerate(ds):
            if (pos + t + i + 1) % n != 0:
                ok = False
                break
        if ok:
            return t
        t += 1

