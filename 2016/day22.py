from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')[2:]
    ns = []
    for l in ls:
        p = l.split()
        x = int(p[0].split('-')[1][1:])
        y = int(p[0].split('-')[2][1:])
        sz = int(p[1][:-1])
        u = int(p[2][:-1])
        a = int(p[3][:-1])
        ns.append((x, y, sz, u, a))
    c = 0
    for i in range(len(ns)):
        for j in range(len(ns)):
            if i != j and ns[i][3] > 0 and ns[i][3] <= ns[j][4]:
                c += 1
    return c


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')[2:]
    ns = {}
    mx = my = 0
    for l in ls:
        p = l.split()
        x = int(p[0].split('-')[1][1:])
        y = int(p[0].split('-')[2][1:])
        mx = max(mx, x)
        my = max(my, y)
        sz = int(p[1][:-1])
        u = int(p[2][:-1])
        ns[(x, y)] = (sz, u)

    emp = None
    for k, (sz, u) in ns.items():
        if u == 0:
            emp = k
            break

    wall = []
    for (x, y), (sz, u) in ns.items():
        if u > 100:
            wall.append((x, y))

    # Move empty to left of goal data
    # Goal is at (mx, 0), need to move to (0, 0)
    # Pattern: move empty around goal, swap, repeat
    # Cost = steps to get empty next to goal + 5*(mx-1) + 1

    # BFS to find path for empty to (mx-1, 0)
    from collections import deque
    q = deque([(emp, 0)])
    vis = {emp}
    d1 = 0
    while q:
        (x, y), d = q.popleft()
        if x == mx - 1 and y == 0:
            d1 = d
            break
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx <= mx and 0 <= ny <= my and (nx, ny) not in vis and (nx, ny) not in wall:
                vis.add((nx, ny))
                q.append(((nx, ny), d+1))

    return d1 + 5 * (mx - 1) + 1

