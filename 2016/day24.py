from typing import Any
from collections import deque
from itertools import permutations


def solve_part_1(input_data: str) -> Any:
    g = input_data.strip().split('\n')
    pts = {}
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if c.isdigit():
                pts[int(c)] = (x, y)

    def bfs(sx, sy, ex, ey):
        q = deque([(sx, sy, 0)])
        v = {(sx, sy)}
        while q:
            x, y, d = q.popleft()
            if x == ex and y == ey:
                return d
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and (nx, ny) not in v and g[ny][nx] != '#':
                    v.add((nx, ny))
                    q.append((nx, ny, d+1))

    dst = {}
    for i in pts:
        for j in pts:
            if i != j:
                dst[(i, j)] = bfs(*pts[i], *pts[j])

    mn = float('inf')
    for p in permutations(range(1, len(pts))):
        d = dst[(0, p[0])]
        for i in range(len(p) - 1):
            d += dst[(p[i], p[i+1])]
        mn = min(mn, d)
    return mn


def solve_part_2(input_data: str) -> Any:
    g = input_data.strip().split('\n')
    pts = {}
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if c.isdigit():
                pts[int(c)] = (x, y)

    def bfs(sx, sy, ex, ey):
        q = deque([(sx, sy, 0)])
        v = {(sx, sy)}
        while q:
            x, y, d = q.popleft()
            if x == ex and y == ey:
                return d
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and (nx, ny) not in v and g[ny][nx] != '#':
                    v.add((nx, ny))
                    q.append((nx, ny, d+1))

    dst = {}
    for i in pts:
        for j in pts:
            if i != j:
                dst[(i, j)] = bfs(*pts[i], *pts[j])

    mn = float('inf')
    for p in permutations(range(1, len(pts))):
        d = dst[(0, p[0])]
        for i in range(len(p) - 1):
            d += dst[(p[i], p[i+1])]
        d += dst[(p[-1], 0)]
        mn = min(mn, d)
    return mn

