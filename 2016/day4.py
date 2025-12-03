from typing import Any
from collections import Counter


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    t = 0
    for l in ls:
        p = l.rfind('-')
        nm = l[:p].replace('-', '')
        r = l[p+1:]
        sid = int(r[:r.index('[')])
        chk = r[r.index('[')+1:-1]
        c = Counter(nm)
        s = sorted(c.items(), key=lambda x: (-x[1], x[0]))[:5]
        if ''.join([x[0] for x in s]) == chk:
            t += sid
    return t


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    for l in ls:
        p = l.rfind('-')
        nm = l[:p]
        r = l[p+1:]
        sid = int(r[:r.index('[')])
        d = ''
        for ch in nm:
            if ch == '-':
                d += ' '
            else:
                d += chr((ord(ch) - ord('a') + sid) % 26 + ord('a'))
        if 'north' in d:
            return sid
