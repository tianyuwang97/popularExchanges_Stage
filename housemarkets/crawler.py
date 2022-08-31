import numpy as np
import random

import sys

sys.path.insert(0, "..")

##########################################
##### CRAWLER LEFT -> RIGHT ##############
##########################################

#apply crawler algorithm of Bade from left to right
#@prefs : prefs of the agents  (single-peaked) prefs[i][] stands for  the preference profile of agent i speciified as a Borda score
#@n : number of agents / houses
#@alloc : initial allocation
#@axis : order of the resources on the single-peaked axis
from housemarkets import allocTools, utility


def crawlerLR(prefs, n, alloc, axis, verbose=False):

    res = []
    lAgents=[]
    lHouses=[]
    nbCycles = 0
    sizeCycles = 0
    maxSizeC = -1
    minSizeC = -1
    nbSwap = 0
    # print("alloc" , alloc)
    #print("axis", axis)
    # init lists lAgents and lHouses
    for i in axis:
        j = 0
        while j<n and alloc[j] != i: # find the agent who holds the ith resource on the axis
            j = j+1
        lAgents.append(j)
        lHouses.append(i)
        res.append(-1)

    while lAgents:# while some  agents / houses are unassigned
        index = 0
        b = 0
        while index < len(lAgents) and not(b):
            #print("index=",index)
            #print("lagents",lAgents)
            a = lAgents[index]
            if (index < len(lAgents) -1 and prefs[a][lHouses[index]] > prefs[a][lHouses[index+1]]) or (index == len(lAgents) -1 and prefs[a][lHouses[index]] < n):
                #print("pref",prefs[a][lHouses[index]],prefs[a][lHouses[index+1]] )
                # search the best unmatched house for the agent
                hmax = lHouses[0]
                id = 0
                idmax = 0
                for h in lHouses[1:]:
                    id = id +1
                    if(prefs[a][h] > prefs[a][hmax]):
                            hmax = h
                            idmax = id
                #assign the house
                res[a] = hmax
                if(index != idmax) :
                    nbCycles = nbCycles +1
                    sizeC = index - idmax +1
                    sizeCycles = sizeCycles + sizeC
                    nbSwap = nbSwap + sizeC - 1
                    if (minSizeC == -1 or sizeC < minSizeC):
                        minSizeC = sizeC
                    if (maxSizeC == -1 or sizeC > maxSizeC):
                        maxSizeC = sizeC
                   # print("match agent", a , " with h",hmax, "size cycle = " , index - idmax +1 , "id", idmax, "index", index)
                #else :
                 #   print("match agent", a, " with h", hmax, "size cycle = 0")
                lAgents.remove(a)
                lHouses.remove(hmax)
                #quit the loop
                b = 1
            index = index +1
        if(not(b)):

                a = lAgents[-1]
                h = lHouses[-1]
                res[a] = h
                lAgents.remove(a)
                lHouses.remove(h)
                #print("no better house match agent", a , " with h",h)
    if nbCycles != 0:
        sizeCycles = sizeCycles / nbCycles
    if verbose :
        return (res, nbCycles, sizeCycles, minSizeC, maxSizeC,nbCycles)
    else :
        return res




def crawlerLR_K (prefs, n, alloc, axis,k):
    res = alloc
    for i in range(k):
        res = crawlerLR(prefs, n, res, axis)
        print(res)
    return res




##########################################
##### CRAWLER RIGHT -> LEFT ##############
##########################################

#@prefs : prefs of the agents  (single-peaked) prefs[i][] stands for  the preference profile of agent i speciified as a Borda score
#@n : number of agents / houses
#@alloc : initial allocation
#@axis : order of the resources on the single-peaked axis
def crawlerRL(prefs, n, alloc, axis):

    res = []
    lAgents=[]
    lHouses=[]
    # init lists lAgents and lHouses
    for i in axis:
        j = 0
        while j<n and alloc[j] != i: # find the agent who holds the ith resource on the axis
            j = j+1
        lAgents.append(j)
        lHouses.append(i)
        res.append(-1)

    while lAgents:# while some  agents / houses are unassigned
        index = len(lAgents) -1
        b = 0
        while index >=0 and not(b):
            a = lAgents[index]
            if (index >0 and prefs[a][lHouses[index]] > prefs[a][lHouses[index-1]]) or (index == 0 and prefs[a][lHouses[index]] < n):
                #print("pref",prefs[a][lHouses[index]],prefs[a][lHouses[index+1]] )
                # search the best unmatched house for the agent
                hmax = lHouses[0]
                for h in lHouses[1:]:
                    if(prefs[a][h] > prefs[a][hmax]):
                            hmax = h
                #assign the house
                res[a] = hmax
                #print("match agent", a , " with h",hmax )
                lAgents.remove(a)
                lHouses.remove(hmax)
                #quit the loop
                b = 1
            index = index -1
        if(not(b)):

                a = lAgents[0]
                h = lHouses[0]
                res[a] = h
                lAgents.remove(a)
                lHouses.remove(h)
                #print("no better house match agent", a , " with h",h)
    return res



def crawlerRL_K (prefs, n, alloc, axis,k):
    res = alloc
    for i in range(k):
        res = crawlerRL(prefs, n, res, axis)
        print(res)
    return res





def test_crawler_way(nAgents, nRuns):
    alloc = allocTools.all_alloc(nAgents, nAgents)
    nAlloc = len(alloc)
    axis = np.arange(nAgents)
    for i in range(nRuns):
        index = random.randint(0,nAlloc-1)
        allocT = allocTools.convertAllocTab(alloc[index])
        prefs = utility.generate_SP_UP(nAgents, nAgents)
        resLR = crawlerLR(prefs,nAgents,allocT, axis)
        print(resLR)
        resRL = crawlerRL(prefs,nAgents,allocT, axis)
        print(resRL)
        assert resLR == resRL


def changeFormatAllocInput(alloc):
    res = []
    for e in alloc :
        res = res + e
    return res

def changeFormatAllocOutput( alloc):
    return [ [e] for e in alloc ]



#prefs=[[1,2,3,4],[4,3,2,1],[3,4,2,1],[3,4,2,1]]
prefs=[[4,3,2,1],[3,4,2,1],[1,2,3,4],[1,2,4,3]]
axis=[0,1,2,3]
alloc=[3,2,0,1]
#
res , n1, n2, min, max, nbSwaps = crawlerLR(prefs,4,alloc,axis, True)
print("left -right : ", res, n1, n2)
res = crawlerRL(prefs,4,alloc,axis)
print("right-left :" ,res)
#
# #crawlerLR_K(prefs,4,alloc,axis,3)
#
# #prefs = [[1, 2, 3, 4, 5, 6, 7], [6, 7, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 7, 6],
# #         [1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 7, 6, 5, 1], [3, 4, 5, 6, 7, 2, 1]]
# prefs = [[5, 4, 3, 2, 1], [3,4,5,2,1], [3,5,4,2,1], [1,2,3,4,5], [3,4,5,2,1]]
# #axis = [0, 1, 2, 3, 4, 5, 6]
# axis = [0, 1, 2, 3, 4]
# alloc = [0, 1, 2, 3, 4]
#
#
# res2 = crawlerLR(prefs,5,alloc, axis)
# print("left -right : ", res2)
# res2 = crawlerRL(prefs,5,alloc, axis)
# print("right-left :" ,res2)
# #crawlerLR_K(prefs,7,alloc,axis,3)
#
#
# test_crawler_way(7,1)
