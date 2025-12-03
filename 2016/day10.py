from typing import Any
from collections import defaultdict


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    b = defaultdict(list)
    r = {}
    for l in ls:
        if l.startswith('value'):
            p = l.split()
            v, bot = int(p[1]), int(p[5])
            b[bot].append(v)
        else:
            p = l.split()
            bot = int(p[1])
            lt, lv = p[5], int(p[6])
            ht, hv = p[10], int(p[11])
            r[bot] = (lt, lv, ht, hv)

    while True:
        for bot, vals in list(b.items()):
            if len(vals) == 2:
                lo, hi = min(vals), max(vals)
                if lo == 17 and hi == 61:
                    return bot
                b[bot] = []
                lt, lv, ht, hv = r[bot]
                if lt == 'bot':
                    b[lv].append(lo)
                if ht == 'bot':
                    b[hv].append(hi)


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    b = defaultdict(list)
    o = {}
    r = {}
    for l in ls:
        if l.startswith('value'):
            p = l.split()
            v, bot = int(p[1]), int(p[5])
            b[bot].append(v)
        else:
            p = l.split()
            bot = int(p[1])
            lt, lv = p[5], int(p[6])
            ht, hv = p[10], int(p[11])
            r[bot] = (lt, lv, ht, hv)

    while any(len(v) == 2 for v in b.values()):
        for bot, vals in list(b.items()):
            if len(vals) == 2:
                lo, hi = min(vals), max(vals)
                b[bot] = []
                lt, lv, ht, hv = r[bot]
                if lt == 'bot':
                    b[lv].append(lo)
                else:
                    o[lv] = lo
                if ht == 'bot':
                    b[hv].append(hi)
                else:
                    o[hv] = hi

    return o[0] * o[1] * o[2]

