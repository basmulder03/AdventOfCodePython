from typing import Any
import hashlib
import re


def solve_part_1(input_data: str) -> Any:
    s = input_data.strip()
    k = []
    i = 0
    while len(k) < 64:
        h = hashlib.md5((s + str(i)).encode()).hexdigest()
        m = re.search(r'(.)\1\1', h)
        if m:
            c = m.group(1)
            for j in range(i+1, i+1001):
                h2 = hashlib.md5((s + str(j)).encode()).hexdigest()
                if c*5 in h2:
                    k.append(i)
                    break
        i += 1
    return k[63]


def solve_part_2(input_data: str) -> Any:
    s = input_data.strip()
    cache = {}
    def h2(n):
        if n in cache:
            return cache[n]
        h = s + str(n)
        for _ in range(2017):
            h = hashlib.md5(h.encode()).hexdigest()
        cache[n] = h
        return h
    k = []
    i = 0
    while len(k) < 64:
        h = h2(i)
        m = re.search(r'(.)\1\1', h)
        if m:
            c = m.group(1)
            for j in range(i+1, i+1001):
                if c*5 in h2(j):
                    k.append(i)
                    break
        i += 1
    return k[63]

