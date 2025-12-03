from typing import Any
import re


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    c = 0
    for l in ls:
        pts = re.split(r'\[|\]', l)
        ok = False
        bad = False
        for i, p in enumerate(pts):
            for j in range(len(p) - 3):
                if p[j] == p[j+3] and p[j+1] == p[j+2] and p[j] != p[j+1]:
                    if i % 2 == 0:
                        ok = True
                    else:
                        bad = True
                        break
            if bad:
                break
        if ok and not bad:
            c += 1
    return c


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    c = 0
    for l in ls:
        pts = re.split(r'\[|\]', l)
        abas = set()
        babs = set()
        for i, p in enumerate(pts):
            for j in range(len(p) - 2):
                if p[j] == p[j+2] and p[j] != p[j+1]:
                    if i % 2 == 0:
                        abas.add((p[j], p[j+1]))
                    else:
                        babs.add((p[j+1], p[j]))
        if abas & babs:
            c += 1
    return c

