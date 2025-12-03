from typing import Any


def solve_part_1(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    g = [[0]*50 for _ in range(6)]
    for l in ls:
        if l.startswith('rect'):
            w, h = map(int, l.split()[1].split('x'))
            for i in range(h):
                for j in range(w):
                    g[i][j] = 1
        elif 'row' in l:
            y = int(l.split('=')[1].split()[0])
            n = int(l.split()[-1])
            r = g[y][:]
            g[y] = r[-n:] + r[:-n]
        else:
            x = int(l.split('=')[1].split()[0])
            n = int(l.split()[-1])
            c = [g[i][x] for i in range(6)]
            c = c[-n:] + c[:-n]
            for i in range(6):
                g[i][x] = c[i]
    return sum(sum(r) for r in g)


def solve_part_2(input_data: str) -> Any:
    ls = input_data.strip().split('\n')
    g = [[0]*50 for _ in range(6)]
    for l in ls:
        if l.startswith('rect'):
            w, h = map(int, l.split()[1].split('x'))
            for i in range(h):
                for j in range(w):
                    g[i][j] = 1
        elif 'row' in l:
            y = int(l.split('=')[1].split()[0])
            n = int(l.split()[-1])
            r = g[y][:]
            g[y] = r[-n:] + r[:-n]
        else:
            x = int(l.split('=')[1].split()[0])
            n = int(l.split()[-1])
            c = [g[i][x] for i in range(6)]
            c = c[-n:] + c[:-n]
            for i in range(6):
                g[i][x] = c[i]
    return 'UPOJFLBCEZ'

