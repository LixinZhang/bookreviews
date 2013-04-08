#!/usr/bin/python
# -*- coding:utf-8 -*-
import math
'''
最优化每个节点的坐标位置，使得相交的线段最少，保证画出的网络图比较稀疏可看性强
'''

people = ['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'),
        ('Mike', 'Joe'),
        ('Miranda', 'Mike'),
        ('Violet', 'Augustus'),
        ('Miranda', 'Willy'),
        ('Charlie', 'Mike'),
        ('Veruca', 'Joe'),
        ('Miranda', 'Augustus'),
        ('Willy', 'Augustus'),
        ('Joe', 'Charlie'),
        ('Veruca', 'Augustus'),
        ('Miranda', 'Joe')]


def crosscount(v):
    '''
    判断两条线段是否相交
    '''
    # Convert the number list into a dictionary of person:(x,y)
    loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total=0
    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i+1,len(links)):
            # Get the locations
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
            den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
            # den==0 if the lines are parallel
            if den==0: continue
            # Otherwise ua and ub are the fraction of the
            # line where they cross
            ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
            ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
        if ua > 0 and ua <1 and ub > 0 and ub < 1 :
            total += 1
    return total
