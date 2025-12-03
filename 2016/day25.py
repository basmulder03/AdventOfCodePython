from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    for a in range(1000):
        r = {'a': a, 'b': 0, 'c': 0, 'd': 0}
        i = 0
        out = []
        cnt = 0
        while i < len(ls) and cnt < 100:
            p = ls[i].split()
            if p[0] == 'cpy':
                v = r[p[1]] if p[1] in r else int(p[1])
                if p[2] in r:
                    r[p[2]] = v
            elif p[0] == 'inc':
                if p[1] in r:
                    r[p[1]] += 1
            elif p[0] == 'dec':
                if p[1] in r:
                    r[p[1]] -= 1
            elif p[0] == 'jnz':
                v = r[p[1]] if p[1] in r else int(p[1])
                if v != 0:
                    j = r[p[2]] if p[2] in r else int(p[2])
                    i += j
                    continue
            elif p[0] == 'out':
                v = r[p[1]] if p[1] in r else int(p[1])
                out.append(v)
                cnt += 1
            i += 1
        if out == [i % 2 for i in range(len(out))]:
            return a


def solve_part_2(input_data: str) -> Any:
    return 'Merry Christmas!'

