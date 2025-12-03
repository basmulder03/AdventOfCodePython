from typing import Any
import hashlib
from collections import deque


def solve_part_1(input_data: str) -> Any:
    s = input_data.strip()
    q = deque([(0, 0, '')])
    while q:
        x, y, p = q.popleft()
        if x == 3 and y == 3:
            return p
        h = hashlib.md5((s + p).encode()).hexdigest()[:4]
        for i, (d, dx, dy) in enumerate([('U',0,-1),('D',0,1),('L',-1,0),('R',1,0)]):
            if h[i] in 'bcdef':
                nx, ny = x + dx, y + dy
                if 0 <= nx < 4 and 0 <= ny < 4:
                    q.append((nx, ny, p + d))


def solve_part_2(input_data: str) -> Any:
    s = input_data.strip()
    q = deque([(0, 0, '')])
    mx = 0
    while q:
        x, y, p = q.popleft()
        if x == 3 and y == 3:
            mx = max(mx, len(p))
            continue
        h = hashlib.md5((s + p).encode()).hexdigest()[:4]
        for i, (d, dx, dy) in enumerate([('U',0,-1),('D',0,1),('L',-1,0),('R',1,0)]):
            if h[i] in 'bcdef':
                nx, ny = x + dx, y + dy
                if 0 <= nx < 4 and 0 <= ny < 4:
                    q.append((nx, ny, p + d))
    return mx

