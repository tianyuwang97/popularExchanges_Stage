import copy
import itertools
import random

import numpy as np
# Génère tous les subsets de l
def subsets(l):
    l = copy.deepcopy(l)
    res = [l]
    s = set(l)
    for i in range(len(l)):
        for sub in set(itertools.combinations(s, i)):
            if len(sub) != 0:
                res.append(list(sub))
    return res


# Génère les subsetsde l d'une taille donnée
def subset(l, size):
    if size == 1:
        return [[i] for i in l]
    else:
        return [list(i) for i in itertools.combinations(l, size)]


# Retourne tous les découpages possible d'une liste en n éléments de taille non nulle
def slices(l, n):
    global resf
    resf = []

    def aux(l, n, restmp):
        if n == len(l):
            return restmp + [[i] for i in l]
        elif n == 1:
            return restmp + [l]
        else:
            for k in range(len(l) + 1 - n):
                resf.append(aux(l[k + 1:], n - 1, restmp + [l[:k + 1]]))

    if n == len(l):
        return [[[i] for i in l]]
    else:
        aux(l, n, [])
        return [i for i in resf if i != None]


# Retourne toutes les permutations de [[1, size]]
def index_permutation(size):
    def aux(size, result, level=0, item=None):
        if level >= size:
            result.append(item[:])
            return
        if item == None:
            item = [-1 for i in range(size)]
        for index in range(size):
            if item[index] < 0:
                item[index] = level
                aux(size, result, level + 1, item)
                item[index] = -1
        return result

    return aux(size, [])


# Génère toutes les alloc possibles
def all_alloc(nb_resources, nb_player):
    res = []
    for l in index_permutation(nb_resources):
        res += slices(l, nb_player)
    return res

def max_tab(tab, size):
    maxC = 0

    for e in range(1, size) :
        if tab[e] > tab[maxC]:
            maxC = e
    return maxC

def max_good_tab(tab,size,tab2,listPre):
    e = 1
    #secondbeforegood=False
    for i in range(e,size):
        val=listPre[i]-1
        #if(tabSH[val]==True):
            #secondbeforegood=True
        if(tab2[val] == True):

            return val

    return -1
def max_bad_tab(tab,size,tab2,listPre):
    e = 2
    #secondbeforegood=False
    for i in range(e,size):
        val=listPre[i]-1
        #if(tabSH[val]==True):
            #secondbeforegood=True


        return val




def max_good_tab2(tab,size,tab2,tabSH,listPre):
    e = 1
    secondbeforegood=False
    for i in range(e,size):
        val=listPre[i]-1
        if(tabSH[val]==True):
            secondbeforegood=True
        if(tab2[val] == True and secondbeforegood==False):

            return val

    return -1



def max_sec_tab(tab, size, tab2) :

    e = 0
    while(e < size and tab2[e] == True ):
        e = e+1
    if e == size :
        return -1
    else :
        maxC = e
        for e2 in range(e+1,size):
            if tab[e2] > tab[maxC] and tab2[e2] == False :
                maxC = e2
        return maxC





# Génère toutes les alloc où les agents ont le même nombre de ressources
def all_even_sized_alloc(nb_resources, nb_resource_per_player):
    res = []
    for r in index_permutation(nb_resources):
        res.append([r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)])
    return res


# Truc le plus moche du monde, test Pareto en testant toutes les alloc possibles
def isPareto(players, nb_resources, allocs):
    def isBetterAll(a, players):
        onebetter = False
        for p in players:
            if p.utility(a[p.num]) < p.selfutility():
                return False
            elif p.utility(a[p.num]) > p.selfutility():
                onebetter = True
        #		if onebetter:
        #				print("\n\t\t!!!!!!!!!!!!!!!!!!\np = " + str(players) + " a = " + str(a) + "\n")
        #				sys.exit(0)
        return onebetter

    if allocs is None:
        allocs = all_alloc(nb_resources, len(players))
    for a in allocs:
        if isBetterAll(a, players):
            return False
    return True

#convert a list of list into a list of resources (for houseallocation only)
def convertAllocTab(alloc):
    res = []
    for e in alloc:
        res.append(e[0])
    return res

#Génère une allocation avec 1 ressource par agent
def generateAlloc( nb_resources):
    alloc = [[i] for i in range(0, nb_resources)]
    random.shuffle(alloc)
    return alloc


def main():
    #random.seed(time.time())


    a=all_alloc(3,3)
    b=all_alloc(3,3)
    c=all_alloc(3,3)
    res=[]
    for i in range(len(a)):
        res.append(a[i])
        for j in range (len(b)):
            res.append(b[j])


    print(a)
main()
