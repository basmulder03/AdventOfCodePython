from typing import Any
from collections import deque
from itertools import combinations


def slv(init):
    def ok(s):
        for i in range(0, len(s), 2):
            if s[i] != s[i+1] and any(s[j] == s[i+1] for j in range(0, len(s), 2) if j != i):
                return False
        return True
    def canon(s):
        pairs = sorted([(s[i], s[i+1]) for i in range(0, len(s), 2)])
        return tuple(x for p in pairs for x in p)
    q = deque([(init, 0)])
    vis = {(init[0], canon(init[1]))}
    while q:
        (e, s), d = q.popleft()
        if all(x == 3 for x in s):
            return d
        for mv in [1, -1]:
            ne = e + mv
            if 0 <= ne < 4:
                idx = [i for i, x in enumerate(s) if x == e]
                for sz in [1, 2]:
                    for c in combinations(idx, sz):
                        ns = list(s)
                        for i in c:
                            ns[i] = ne
                        ns = tuple(ns)
                        cs = (ne, canon(ns))
                        if ok(ns) and cs not in vis:
                            vis.add(cs)
                            q.append(((ne, ns), d + 1))


def solve_part_1(input_data: str) -> Any:
    return slv((0, (0, 0, 1, 2, 1, 2, 1, 2, 1, 2)))


def solve_part_2(input_data: str) -> Any:
    return slv((0, (0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2)))
