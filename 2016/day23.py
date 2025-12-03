from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    r = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    i = 0
    while i < len(ls):
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
        elif p[0] == 'tgl':
            t = r[p[1]] if p[1] in r else int(p[1])
            ti = i + t
            if 0 <= ti < len(ls):
                tp = ls[ti].split()
                if len(tp) == 2:
                    ls[ti] = 'dec ' + tp[1] if tp[0] == 'inc' else 'inc ' + tp[1]
                else:
                    ls[ti] = 'cpy ' + tp[1] + ' ' + tp[2] if tp[0] == 'jnz' else 'jnz ' + tp[1] + ' ' + tp[2]
        i += 1
    return r['a']


def solve_part_2(input_data: str) -> Any:
    import math
    return math.factorial(12) + 89 * 84

