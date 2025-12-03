from typing import Any
from collections import deque


def solve_part_1(input_data: str) -> Any:
    n = int(input_data.strip())
    def w(x, y):
        v = x*x + 3*x + 2*x*y + y + y*y + n
        return bin(v).count('1') % 2 == 1
    q = deque([(1, 1, 0)])
    vis = {(1, 1)}
    while q:
        x, y, d = q.popleft()
        if x == 31 and y == 39:
            return d
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if nx >= 0 and ny >= 0 and (nx, ny) not in vis and not w(nx, ny):
                vis.add((nx, ny))
                q.append((nx, ny, d+1))


def solve_part_2(input_data: str) -> Any:
    n = int(input_data.strip())
    def w(x, y):
        v = x*x + 3*x + 2*x*y + y + y*y + n
        return bin(v).count('1') % 2 == 1
    q = deque([(1, 1, 0)])
    vis = {(1, 1)}
    while q:
        x, y, d = q.popleft()
        if d >= 50:
            continue
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if nx >= 0 and ny >= 0 and (nx, ny) not in vis and not w(nx, ny):
                vis.add((nx, ny))
                q.append((nx, ny, d+1))
    return len(vis)

