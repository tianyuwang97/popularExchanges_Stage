import numpy as np
import copy
import time
import random
import itertools

#from housemarkets
import allocTools, player


# Choisit une paire d'agents aléatoirement et applique le swap entre ces agents si possible, return False si un swap realise,
# True si plus  aucun swap réalisable
def swap_aux_alea_uni_agent(players, display):
    idAg1 = random.randint(0, len(players)-1)
    idAg2 = random.randint(0, len(players)-2)
    if(idAg1 <= idAg2) : # garantit que idAg1 != idAg2 en gardant une distribution uniforme
        idAg2 = idAg2 +1

    lSwap = []
    p1 = players[idAg1]
    p2 = players[idAg2]


    if ((p1.utility(p2.bundle) >= p1.selfutility() and p2.utility(p1.bundle) > p2.selfutility())
        or (p1.utility(p2.bundle) > p1.selfutility() and p2.utility(p1.bundle) >= p2.selfutility())):

        lSwap.append([p1, p1.bundle, p2, p2.bundle])  # on ajoute le swap dans la liste des swaps possibles

    if (lSwap):  # some swaps are possible
        # print("lswap = ", lSwap, "len=",len(lSwap))
        swapDo = lSwap[0]
        if display:
            print("{} gives {} to {} who gives  {}".format(swapDo[0].num, swapDo[1], swapDo[2].num, swapDo[3]))

        r1 = list(swapDo[1])
        r2 = list(swapDo[3])
        swapDo[0].swap(r1, r2)
        swapDo[2].swap(r2, r1)

        return 0

    # on doit déterminer si des swaps sont encore réalisables

    for p1 in players:
        for p2 in players[p1.num + 1:]:

            if ((p1.utility(p2.bundle) >= p1.selfutility()
                 and p2.utility(p1.bundle) > p2.selfutility())
                    or (p1.utility(p2.bundle) > p1.selfutility()
                        and p2.utility(p1.bundle) >= p2.selfutility())):
                return -1


    #							print("No swap")
    return 1




# Teste tous les swaps possibles et applique un de ceux realisables choisi aleatoirement, return False si un swap realise, True sinon
def swap_aux_alea_uni(players, display):
    lSwap = []

    for p1 in players:
        for p2 in players[p1.num + 1:]:

            if ((p1.utility(p2.bundle) >= p1.selfutility()
                 and p2.utility(p1.bundle) > p2.selfutility())
                    or (p1.utility(p2.bundle) > p1.selfutility()
                        and p2.utility(p1.bundle) >= p2.selfutility())):
                lSwap.append([p1, p1.bundle, p2, p2.bundle])  # on ajoute le swap dans la liste des swaps possibles

    if (lSwap):  # some swaps are possible
        # print("lswap = ", lSwap, "len=",len(lSwap))
        ind = random.randint(0, len(lSwap) - 1)
        # print("ind", ind)
        swapDo = lSwap[ind]
        if display:
            print("{} gives {} to {} who gives  {}".format(swapDo[0].num, swapDo[1], swapDo[2].num, swapDo[3]))

        r1 = list(swapDo[1])
        r2 = list(swapDo[3])
        swapDo[0].swap(r1, r2)
        swapDo[2].swap(r2, r1)

        return False
    #							print("No swap")
    return True


# Test tous les swaps possibles et applique un de ceux realisables choisi aleatoirement PARMI LES SWAPS RATIONNELS en priorisant les agents qui n'ont pas encore echange
#  return False si un swap realise, True sinon
def swap_aux_alea_prio(players, display, tab_agents):
    lSwap = []
    lSwapPrio = []

    for p1 in players:
        for p2 in players[p1.num + 1:]:
            if ((p1.utility(p2.bundle) >= p1.selfutility()
                 and p2.utility(p1.bundle) > p2.selfutility())
                    or (p1.utility(p2.bundle) > p1.selfutility()
                        and p2.utility(p1.bundle) >= p2.selfutility())):
                lSwap.append([p1, p1.bundle, p2, p2.bundle])  # on ajoute le swap dans la liste des swaps possibles
                if not (tab_agents[p1.num]):
                    if not (tab_agents[p2.num]):
                        lSwapPrio.append([p1, p1.bundle, p2, p2.bundle])

    if (lSwapPrio):  # some swaps  involving priority agents are possible
        ind = random.randint(0, len(lSwapPrio) - 1)
        # print("ind", ind)
        swapDo = lSwapPrio[ind]
        if display:
            print("Prio : {} gives {} to {} who gives  {}".format(swapDo[0].num, swapDo[1], swapDo[2].num, swapDo[3]))

        r1 = list(swapDo[1])
        r2 = list(swapDo[3])
        swapDo[0].swap(r1, r2)
        swapDo[2].swap(r2, r1)
        tab_agents[swapDo[0].num] = 1
        tab_agents[swapDo[2].num] = 1

        return False

    elif (lSwap):  # some swap with agents who have already exchanged
        # print("lswap = ", lSwap, "len=",len(lSwap))
        ind = random.randint(0, len(lSwap) - 1)
        # print("ind", ind)
        swapDo = lSwap[ind]
        if display:
            print("Non prio {} gives {} to {} who gives  {}".format(swapDo[0].num, swapDo[1], swapDo[2].num, swapDo[3]))

        r1 = list(swapDo[1])
        r2 = list(swapDo[3])
        swapDo[0].swap(r1, r2)
        swapDo[2].swap(r2, r1)
        for i in range(len(players)):
            tab_agents[i] = 0
        tab_agents[swapDo[0].num] = 1
        tab_agents[swapDo[2].num] = 1

        return False
    #							print("No exchange")
    return True


# Choisit un swap aléatoirement parmi l'ensemble des swaps en pirorisant les agents qui n'ont pas encore échangé
# return 0 si plus aucun swao rationnel n'est possible, 1 si un swap implémenté, -1 sinon (swap rationnel possible mais un swap non rationnel a été selectionné ou plus d'agents prioritaires)
def swap_aux_alea_prioV2(players, display, tab_agents):
    swapRat = False
    swapRatPrio=False
    lAgentPrio = []
    if display :
        print("***************************")
    for p1 in players:
        if not (tab_agents[p1.num]):
            lAgentPrio.append(p1.num)
        for p2 in players[p1.num + 1:]:
            if ((p1.utility(p2.bundle) >= p1.selfutility()
                 and p2.utility(p1.bundle) > p2.selfutility())
                    or (p1.utility(p2.bundle) > p1.selfutility()
                        and p2.utility(p1.bundle) >= p2.selfutility())):
                            if display :
                                print("echange rat possible entre {} et {}".format(p1.num, p2.num))
                            swapRat = True # on ajoute le swap dans la liste des swaps possibles
                            if not (tab_agents[p1.num]) and not (tab_agents[p2.num]):
                                swapRatPrio = True

    if display :
        print("***************************")
    if(not swapRat):
        return 0
    if display :
        print ("liste prio {}".format(lAgentPrio))
    if (len(lAgentPrio)>1 and swapRatPrio):  # at least two agents have priority



        numP1 = lAgentPrio[random.randint(0, len(lAgentPrio)-1)]
        numP2 = lAgentPrio[random.randint(0, len(lAgentPrio)-1)]
        while(numP1 == numP2):
            numP2=lAgentPrio[random.randint(0, len(lAgentPrio)-1)]



        pp1 = players[numP1]
        pp2 = players[numP2]
        bund1 = pp1.bundle.copy()
        bund2 = pp2.bundle.copy()

        if display:
            print("PrioV2 : {} should exchange with {} ".format(pp1.num, pp2.num))

        if((pp1.utility(bund2) >= pp1.selfutility()
            and pp2.utility(bund1) > pp2.selfutility())
                or (pp1.utility(bund2) > pp1.selfutility()
                    and pp2.utility(bund1) >= pp2.selfutility())):
            if display :
                print("le deal est rationnel")
            pp1.swap(bund1, bund2)
            pp2.swap(bund2, bund1)
            lAgentPrio.remove(numP1)
            lAgentPrio.remove(numP2)
            tab_agents[pp1.num] = 1
            tab_agents[pp2.num] = 1
            exchange = True
            return 1
        else:
            #lCombi.pop(ind1)
            lAgentPrio.remove(numP1)
            lAgentPrio.remove(numP2)
            tab_agents[pp1.num] = 1
            tab_agents[pp2.num] = 1
            return -1

    else:  # some rational swaps are still possible
        # print("lswap = ", lSwap, "len=",len(lSwap))
        for i in range(len(players)):
            tab_agents[i] = 0
        return -1
    #							print("No exchange")
    return -1


# Test tous les swaps possibles et applique le premier realisable, return False si un swap realise, True sinon
def swap_aux_round_robin(players,  indiceAg, display):
    #print("swap round robin indice ag", indiceAg)
    nbP = len(players)
    i = indiceAg
    first = True
    while ( first == True or  i != indiceAg ) :
       # print("\t",i, " over ", nbP)
        p1 = players[i]
        for p2 in players:
            b1 = list(p1.bundle)
            b2 = list(p2.bundle)
            if ((p1.utility(b2) >= p1.selfutility()
                 and p2.utility(b1) > p2.selfutility())
                    or (p1.utility(b2) > p1.selfutility()
                        and p2.utility(b1) >= p2.selfutility())):
                if display:
                    print("{} gives {} to {} who gives  {}".format(p1.num, b1, p2.num, b2))
                p1.swap(b1, b2)
                p2.swap(b2, b1)
                if( i == nbP -1) :
                    return 0
                else :
                    return i +1
        first = False
        if (i == nbP-1):
            i = 0
        else:
            i = i+1
    #							print("No exchange")
    return -1

# Test tous les swaps possibles et applique le premier realisable, return False si un swap realise, True sinon
def swap_aux_round_robin_pairs(players, display):
    n = len(players)
    k = 1 #difference between the agent in the pairs
    i= 0 # id of the first player in the pair
    while k  < n:
        i= 0

        while i<= k:

            j = i
            while j < n and j+k < n :

               # print("pairs : (", j , ", ", j+k , " )\n")
                p1 =players[j]
                p2 = players [j +k]
                b1 = list(p1.bundle)
                b2 = list(p2.bundle)
                if ((p1.utility(b2) >= p1.selfutility()
                     and p2.utility(b1) > p2.selfutility())
                        or (p1.utility(b2) > p1.selfutility()
                            and p2.utility(b1) >= p2.selfutility())):
                    if display:
                        print("{} gives {} to {} who gives  {}".format(p1.num, b1, p2.num, b2))
                    p1.swap(b1, b2)
                    p2.swap(b2, b1)
                    return False
                j = j+k+1
            i = i+1
        k = k+1
    return True



# give the priority to the worst off agent
def swap_aux_worst(players, display):
    # order agent on their individual utility
    playersBis = copy.deepcopy(players)
    playersBis=sorted(playersBis, key=lambda player: player.selfutility())
    #print("swap worst", playersBis)
    # find an exchange
    for i in range(len(playersBis)):
        p1Bis = playersBis[i]
        for j in range(i + 1, len(playersBis)):
            p2Bis = playersBis[j]
            p1 = players[p1Bis.num]
            p2 = players[p2Bis.num]
            b1 = list(p1.bundle)
            b2 = list(p2.bundle)
            if ((p1.utility(b2) >= p1.selfutility()
                 and p2.utility(b1) > p2.selfutility())
                    or (p1.utility(b2) > p1.selfutility()
                        and p2.utility(b1) >= p2.selfutility())):
                if display:
                    print("{} gives {} to {} who gives  {}".format(p1.num, b1, p2.num, b2))
                p1.swap(b1, b2)
                p2.swap(b2, b1)
                return False
    #							print("No exchange")
    return True


# Run swap until a stable allocation
def swap(initial, utilities, u,  test_Pareto=False, test_frustrating=False,
         test_sequenceable=False, display=False, metho_swap=0):
    # metho_swap = 0: roudn robin, 1: alea uniforme, 2: alea uniforme sur les deals rationnels avec priorite aux agents n'ayant pas encore fait d'echanges,
    # 3: swap with the worst off agents first, 4 : round robin on pairs,  5 : alea uniform sur les agents, 6 : alea uniforme sur les agents avec priorite aux agents n'ayant pas encore fait d'echanges,

    # Initialisation des agents
    initial = copy.deepcopy(initial)
    players = [player.Player(i, initial[i], utilities[i], u) for i in range(len(initial))]
    nb_resources = sum([len(i) for i in initial])
    nbswap = 0

    if display:
        print("\nINIT")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        print("\nSWAP")

    # Tant qu'il y a des swaps possible, on les applique
    finished = False
    tab_ag = [0 for i in range(len(initial))]

    indiceAg = 0

    while not finished:
        if metho_swap == 0:
            indiceAg = swap_aux_round_robin(players,indiceAg, display)
            if(indiceAg == -1):
                    finished = True
        elif metho_swap == 1:
            finished = swap_aux_alea_uni(players, display)
        elif metho_swap == 2:
            finished = swap_aux_alea_prio(players, display, tab_ag)
        elif metho_swap == 3:
            finished = swap_aux_worst(players, display)
        elif metho_swap == 4:
            finished = swap_aux_round_robin_pairs(players, display)
        elif metho_swap == 5:
            finAux = swap_aux_alea_uni_agent(players, display)
            if finAux == 1:
                finished = True
            elif finAux == -1:  # il reste des échanges mais pas d'échange implémenté à ce tour
                finished = False
                nbswap = nbswap - 1
            else:
                finished = False
        else :
            finAux = swap_aux_alea_prioV2(players, display, tab_ag)
            if finAux == 0:
                finished = True
            elif finAux == -1:  # il reste des échanges mais pas d'échange implémenté à ce tour
                finished = False
                nbswap = nbswap - 1
            else:
                finished = False

        if(not finished):
            nbswap = nbswap +1
    if display:
        print("\nEND")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

    final =np.zeros((len(players),1), dtype=int)
    for p in players:
        final[p.num] = p.bundle
    #print("nb swap "+ str(nbswap))
    return final, nbswap




# Print a run of swaps
def print_swap(nb_player, nb_resource_per_player, u, pref):
    nb_resources = nb_player * nb_resource_per_player
    init = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    p = pref(nb_player, nb_resources)
    print("PREFERENCES")
    for a in range(len(p)):
        print("{} : {}".format(a, p[a]))
    return swap(init, p, u, display=True)


# Select and apply a swap among bilateral swaps and cycle of size 3
def C3_aux_alea(players, display):
    # print("*******************C 3****************")
    lCycle = []
    # find all cycles of size 3
    for p1 in players:
        for p2 in players[p1.num + 1:]:
            for p3 in players[p1.num + 1:]:
                if p2.num != p3.num:
                    # print ("p1 =",p1.num, " p2 = ", p2.num, "p3= ", p3.num)
                    if ((p1.utility(p2.bundle) > p1.selfutility()
                         and p2.utility(p3.bundle) >= p2.selfutility()
                         and p3.utility(p1.bundle) >= p3.selfutility())
                            or (p1.utility(p2.bundle) >= p1.selfutility()
                                and p2.utility(p3.bundle) > p2.selfutility()
                                and p3.utility(p1.bundle) >= p3.selfutility())
                            or (p1.utility(p2.bundle) >= p1.selfutility()
                                and p2.utility(p3.bundle) >= p2.selfutility()
                                and p3.utility(p1.bundle) > p3.selfutility())):
                        lCycle.append([3, p1, p1.bundle, p2, p2.bundle, p3,
                                       p3.bundle])  # on ajoute le swap dans la liste des swaps possibles
                    # print("{} donne {} et recoit {},{} donne {}et recoit {}, {} donne {} et recoit {} ".format(p1.num, p1.bundle,
                    #															   p2.bundle, p2.num,
                    #												   p2.bundle, p3.bundle,
                    #												   p3.num, p3.bundle,
                    #												   p1.bundle))
    # find all cycles of size 2 ie. swap deals

    for p1 in players:
        for p2 in players[p1.num + 1:]:

            if ((p1.utility(p2.bundle) >= p1.selfutility()
                 and p2.utility(p1.bundle) > p2.selfutility())
                    or (p1.utility(p2.bundle) > p1.selfutility()
                        and p2.utility(p1.bundle) >= p2.selfutility())):
                lCycle.append([2, p1, p1.bundle, p2, p2.bundle])

    if (lCycle):  # some exchanges are possible
        # print("lswap = ", lSwap, "len=",len(lSwap))
        ind = random.randint(0, len(lCycle) - 1)
        # print("ind", ind)
        swapDo = lCycle[ind]
        if swapDo[0] == 3:  # the selected swap is a deal involving 3 agents
            r1 = list(swapDo[2])
            r2 = list(swapDo[4])
            r3 = list(swapDo[6])
            if display:
                print(
                    "echange selec : {} donne {} et recoit {},{} donne {}et recoit {}, {} donne {} et recoit {} ".format(
                        swapDo[1].num, r1, r2, swapDo[3].num, r2, r3, swapDo[5].num, r3, r1))

            swapDo[1].swap(r1, r2)
            swapDo[3].swap(r2, r3)
            swapDo[5].swap(r3, r1)
            return False
        else:  # the selected swap is a bilateral deal
            if display:
                print("{} gives {} to {} who gives  {}".format(swapDo[1].num, swapDo[2], swapDo[3].num, swapDo[4]))
            r1 = list(swapDo[2])
            r2 = list(swapDo[4])
            swapDo[1].swap(r1, r2)
            swapDo[3].swap(r2, r1)
            return False

        #print("No exchange")
    return True


# Run C2 and C3 exchanges until a stable allocation is reached
def cycle3(initial, utilities, u, allocs=None, test_Pareto=False, test_frustrating=False,
       test_sequenceable=False, display=False):
    # Initialisation des agents
    initial = copy.deepcopy(initial)
    players = [player.Player(i, initial[i], utilities[i], u) for i in range(len(initial))]
    nb_resources = sum([len(i) for i in initial])

    if display:
        print("\nINIT")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        print("\nSWAP")

    # While some swaps are still possible
    finished = False
    nbcycles = 0
    while not finished:
        finished = C3_aux_alea(players, display)
        if( not finished):
            nbcycles = nbcycles + 1
    # if display:
    #	for p in players:
    #		print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
    #	print("\n")
    if display:
        print("\nEND")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

    final = np.zeros((len(players), 1), dtype=int)
    for p in players:
        final[p.num] = p.bundle
    return final, nbcycles


# Compte le nombre d'alloc PO sur nb_try
def count_nb_Pareto(nb_try, f, nb_player, nb_resource_per_player, preferences, even_size=True):
    initTime = time.time()
    nb_resources = nb_player * nb_resource_per_player
    print("Nombre d'Optimum de Pareto pour {} joueurs et {} ressources avec la fonction {}, {} essais".format(
        nb_player, nb_resources, f.__name__, nb_try))

    if even_size:
        allocs = allocTools.all_even_sized_alloc(nb_resources, nb_resource_per_player)
    else:
        allocs = allocTools.all_alloc(nb_resources, nb_player)
    print("Nombre d'allocations differentes : {}".format(len(allocs)))

    res = 0
    init = []
    tmp = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    print("Allocation initiale : {}".format(init))

    for i in range(nb_try):
        if i % (nb_try / 10) == 0:
            print("Essai {} : nombre de non Pareto {} sur {}".format(i, res, i))
        if not swap(init, preferences(nb_player, nb_resources), f, allocs, test_Pareto=True):
            res += 1
    print("Nombre d etat stationnaire de swap non Pareto optimal : {} sur {}".format(res, nb_try))
    print("Temps de calcul du nombre de Pareto : {} secondes".format(time.time() - initTime))
    return res


# Compte le nombre d'alloc sequenceable sur nb_try
def count_nb_Seq(nb_try, f, nb_player, nb_resource_per_player, preferences, even_size=True):
    initTime = time.time()
    nb_resources = nb_player * nb_resource_per_player
    print("Nombre d'equilibre sequenceable pour {} joueurs et {} ressources avec la fonction {}, {} essais".format(
        nb_player, nb_resources, f.__name__, nb_try))

    if even_size:
        allocs = allocTools.all_even_sized_alloc(nb_resources, nb_resource_per_player)
    else:
        allocs = allocTools.all_alloc(nb_resources, nb_player)
    print("Nombre d'allocations differentes : {}".format(len(allocs)))

    res = 0
    init = []
    tmp = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    print("Allocation initiale : {}".format(init))

    for i in range(nb_try):
        if i % (nb_try / 10) == 0:
            print("Essai {} : nombre de non sequenceable {} sur {}".format(i, res, i))
        if not swap(init, preferences(nb_player, nb_resources), f, allocs, test_sequenceable=True):
            res += 1
    print("Nombre d'etat stationnaire de swap non sequenceable optimal : {} sur {}".format(res, nb_try))
    print("Temps de calcul du nombre de sequenceable : {} secondes".format(time.time() - initTime))
    return res



