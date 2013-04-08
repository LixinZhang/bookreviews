#!/usr/bin/python
#!-*- coding:utf-8 -*-
import time
import random
import math

people = [('Seymour','BOS'),('Franny','DAL'),('Zooey','CAK'),('Walt','MIA'),('Buddy','ORD'),('Les','OMA')]

#LaGuardia airport in New York
destination = 'LGA'
def getminutes(t) :
    x = time.strptime(t,'%H:%M')
    return x[3] * 60 + x[4]

def printschedule(r) :
    for d in range(len(r) / 2) :
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin,destination)][r[d]]
        ret = flights[(destination,origin)][r[d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,out[0],out[1],out[2],\
                ret[0],ret[1],ret[2])

def schedulecost(sol) :
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) / 2) :
        origin = people[d][1]
        outbound  = flights[(origin,destination)][int(sol[d])]
        returnf = flights[(destination,origin)][int(sol[d+1])]

        #Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        #Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]) : latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(outbound[0]) : earliestdep = getminutes(outbound[0])
    
    totalwait = 0
    for d in range(len(sol) / 2) :
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(sol[d])]
        returnf = flights[(destination,origin)][int(sol[d+1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep
    #Does this solution require an extra day of car rental ? That'll be $50.
    if latestarrival > earliestdep : totalprice += 50
    return totalprice + totalwait


################Some methods to solve this problem################
def randomoptimize(domain, costf) :
    '''
    随机选取可能的解，通过多次迭代，寻找可能的最优解
    '''
    best = 999999999
    bestr = None 
    for i in range(1000) :
        #Create a random solution
        r = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        #Get the cost
        cost = costf(r)
        if cost < best :
            best = cost
            bestr = r
    return bestr

def hillclimb(domain,costf) :
    #Create a random solution
    sol = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
    while True :
        #Create list of neighboring solutions
        neighbors = []
        for j in range(len(domain)) :
            #One away in each direction
            if sol[j] > domain[j][0] :
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
            if sol[j] < domain[j][1] :
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
        current = costf(sol) 
        best = current
        for j in range(len(neighbors)) :
            cost = costf(neighbors[j])
            if cost < best :
                best = cost
                sol = neighbors[j]
        #if there's no improvement, then we've reached the top
        if best == current :
            break
    return sol

def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1) :
    #Initalize the values randomly
    vec = [float(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
    while T > 0.1 :
        #Choose one of the indices 
        i = random.randint(0,len(domain)-1)
        #Choose a direction to change it
        dir = random.randint(-step,step)
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1] : vecb[i] = domain[i][1]

        #Calculate the current cost and the new cost
        ea = costf(vec) 
        eb = costf(vecb)
        p = pow(math.e,(-eb-ea)/T)
        # Is it better, or does it make the probability
        if (eb<ea or random.random() < p) :
            vec = vecb
        #Decrease the temperature
        T = T*cool
    return vec

def geneticoptimize(domain, costf, popsize=50, step=1, mutprod=0.2, elite=0.2, maxiter=100) :
    #变异操作
    def mutate(vec) :
        i = random.randint(0,len(domain) - 1) 
        if random.random() < 0.5 and vec[i] > domain[i][0] :
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
        elif vec[i] < domain[i][1] :
            return vec[0:i] + [vec[i] + step] + vec[i+1:]
        return vec
    #交叉操作
    def crossover(r1, r2) :
        i = random.randint(1,len(domain)-2)
        return r1[0:i] + r2[i:]
    #build the initial population
    pop = []
    for i in range(popsize) :
        vec  = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        pop.append(vec) 
    #How many winners from each generation?
    topelite = int(elite * popsize)
    #Main loop
    for i in range(maxiter) :
        scores = [(costf(v),v) for v in pop]
        scores.sort()
        ranked = [v for (s,v) in scores]
        # Start with the pure winners
        pop = ranked[0:topelite]
        while len(pop) < popsize :
            if random.random() < mutprod :
                c = random.randint(0,topelite)
                pop.append(mutate(ranked[c]))
            else :
                # Crossover
                c1 = random.randint(0,topelite)
                c2 = random.randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))
            # print current best score
        print scores[0][0]
    return scores[0][1]

if __name__ == '__main__' :
    #test schedule
    s = [1,4,3,2,7,3,6,3,2,4,5,3]
    flights = {}
    for line in file('schedule.txt') :
        origin,dest,depart,arrive,price = line.strip().split(',')
        flights.setdefault((origin,dest),[])
        # Add details to the list of possible flights
        flights[(origin,dest)].append((depart,arrive,int(price)))
    print len(flights)
    printschedule(s)
    domain = [(0,8)] * (len(people)*2)
#    s = randomoptimize(domain, schedulecost)
#    print schedulecost(s)
    #s = hillclimb(domain,schedulecost)
    #s = annealingoptimize(domain,schedulecost)
    s = geneticoptimize(domain,schedulecost)
    print schedulecost(s)

    
