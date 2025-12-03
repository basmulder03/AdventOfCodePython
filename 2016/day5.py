from typing import Any
import hashlib


def solve_part_1(input_data: str) -> Any:
    d = input_data.strip()
    pw = ''
    i = 0
    while len(pw) < 8:
        h = hashlib.md5((d + str(i)).encode()).hexdigest()
        if h.startswith('00000'):
            pw += h[5]
        i += 1
    return pw


def solve_part_2(input_data: str) -> Any:
    d = input_data.strip()
    pw = ['_'] * 8
    i = 0
    f = 0
    while f < 8:
        h = hashlib.md5((d + str(i)).encode()).hexdigest()
        if h.startswith('00000'):
            p = h[5]
            if p.isdigit():
                pos = int(p)
                if pos < 8 and pw[pos] == '_':
                    pw[pos] = h[6]
                    f += 1
        i += 1
    return ''.join(pw)

