from typing import Any

def solve_part_1(input_data: str) -> Any:
    g=[list(l) for l in input_data.strip().split('\n')]
    R,C=len(g),len(g[0])
    d=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    cnt=0
    for r in range(R):
        for c in range(C):
            if g[r][c]=='@':
                a=sum(1 for dr,dc in d if 0<=r+dr<R and 0<=c+dc<C and g[r+dr][c+dc]=='@')
                if a<4:cnt+=1
    return cnt

def solve_part_2(input_data: str) -> Any:
    g=[list(l) for l in input_data.strip().split('\n')]
    R,C=len(g),len(g[0])
    d=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    tot=0
    while 1:
        acc=[]
        for r in range(R):
            for c in range(C):
                if g[r][c]=='@':
                    a=sum(1 for dr,dc in d if 0<=r+dr<R and 0<=c+dc<C and g[r+dr][c+dc]=='@')
                    if a<4:acc.append((r,c))
        if not acc:break
        for r,c in acc:g[r][c]='.'
        tot+=len(acc)
    return tot
