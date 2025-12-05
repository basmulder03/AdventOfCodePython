from typing import Any

def solve_part_1(input_data: str) -> Any:
    l=input_data.strip().split('\n')
    b=0
    for i,x in enumerate(l):
        if x=='':b=i;break
    r=[]
    for i in range(b):
        p=l[i].split('-')
        r.append((int(p[0]),int(p[1])))
    ids=[int(l[i]) for i in range(b+1,len(l))]
    c=0
    for i in ids:
        for s,e in r:
            if s<=i<=e:c+=1;break
    return c

def solve_part_2(input_data: str) -> Any:
    l=input_data.strip().split('\n')
    b=l.index('')
    r=[(int(l[i].split('-')[0]),int(l[i].split('-')[1])) for i in range(b)]
    r.sort()
    m=[]
    for s,e in r:
        if m and s<=m[-1][1]+1:m[-1]=(m[-1][0],max(m[-1][1],e))
        else:m.append((s,e))
    return sum(e-s+1 for s,e in m)
