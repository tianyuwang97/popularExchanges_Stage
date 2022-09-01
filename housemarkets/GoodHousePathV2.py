import numpy as np
import copy
import random
import time
#from housemarkets import allocTools, player, utility, classeState
import allocTools, player, utility, classeState

def exchAlreadyDone(lAlloc, alloCurr,  idAgents, idRes, nb_agents, size_exch = 3):

    print("echange a tester  agents {} resources {} allocourante = {}".format(idAgents, idRes, alloCurr))
    for i in lAlloc :
        print("\t alloc à tester {}".format(i))
        if(i.equalAlloc(alloCurr, nb_agents)) :
            print("allocation deja rencontrée {} \n allocourante = {}".format(i, alloCurr))
            nbe = i.alreadyDoneExch(idAgents, idRes, size_exch)
            if nbe != None :
                return  nbe
    return None

def already_seen(lAlloc, alloc, n) :
    #print("alloc à trouver dans already seen {}".format(alloc))
    for e in lAlloc:
        if e.alreadySeenAlloc(alloc, n ) :
            #print("retour de already seen : {}".format(e))
            return e
    return None

def getAlloc(players, n):
    res = [-1] *n
    for i in range(n) :
        p = players[i]
        res[p.num] = p.bundle[0]
    #print("alloc calculée {}".format(res))
    return res
def transfer(preferences):
    list=[]
    for i in range(len(preferences)):

        sorted_nums = sorted(enumerate(preferences[i]), key=lambda x: x[1], reverse=True)
        idx = [i[0]+1 for i in sorted_nums]
        nums = [i[1] for i in sorted_nums]
        list.append(idx)


    return list

def verif_popular(players, nbItems, FH, SH ):
    for p in players :
        #if(p.bundle[0] != FH[p.num] and p.bundle[0] !=SH[p.num] and p.bundle[0]!= GH[p.num]):
        if (p.bundle[0] != FH[p.num] and p.bundle[0] != SH[p.num] ):
            # print("problem de ",p)
            # print(SH[p.num])

            return False
    return True


def goodhouse_path_to_popular(initial, utilities, u, display=False):
    # Initialisation des agents
    initial = copy.deepcopy(initial)
    listWrong = []

    players = [player.Player(i, initial[i], utilities[i], u) for i in range(len(initial))]
    nb_resources = sum([len(i) for i in initial])

    nbCycles = 0

    # revert the allocation to easily access to the owner of a house
    house_to_agents = [-1] * nb_resources

    print(house_to_agents)
    print(utilities)
    print(players)

    print(nb_resources)
    # print(nb_resources)
    for i in range(nb_resources):
        # print(i)
        # print(initial[i])
        b = initial[i]
        # print(b)
        # print(b[0])
        house_to_agents[b[0]] = i
    print(house_to_agents)
    nbExch = 0
    stop = (nb_resources ** 2 - nb_resources + 2) / 2

    if display:
        print("\nINIT")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

    nbItem = len(players)

    # initi FH, SH
    listPre = transfer(utilities)
    print(listPre)
    FH = [-1] * nb_resources

    GH = [-1] * nb_resources

    isFH = [False] * nb_resources

    isSH = [False] * nb_resources
    SH = [-1] * nb_resources
    i = 0
    for p in players:
        m1 = p.get_best_item(nb_resources)  # m1 indice de FH
        # print("M1:")
        isFH[m1] = True
        FH[p.num] = m1

    for p in players:
        m2 = p.get_best_sec_item(nb_resources, isFH)
        # print(m2)
        isSH[m2] = True
        SH[p.num] = m2

    # print(isFH)
    # print(isSH)
    for p in players:
        mg = p.get_good_item(nb_resources, isFH, listPre[p.num])
        GH[p.num] = mg
    print("good house", GH)
    print("second house", SH)

    # First part of the algorithm  on change le deuxime agent qui prend le GOOD HOUSE not First HOUSE

    bad_agents = []  # agents holding a bad house (not a first or a second house)
    already_Done = [[[[] for k in range(nb_resources)] for j in range(nb_resources)] for i in range(nb_resources)]
    lAlloc = []  # list of the allocation seen and the list of exchanges for each allocation
    lAlloc.append(classeState.StateAlloc(getAlloc(players, nb_resources)))
    nbe = -1

    # good_agents=[]  #agents holding a good house
    # print("agents with good houses")

    print("agents with bad houses:")
    for p in players:
        if (FH[p.num] != p.bundle[0] and SH[p.num] != p.bundle[0] and GH[p.num] != p.bundle[0]):
            bad_agents.append(p)
            print("bad house for {}".format(p.num))
    # if(len(bad_agents)  != 0 and exception2):
    #     rep=False
    #     listWrong.append(house_to_agents)
    #     print("house_to",house_to_agents)
    #     return (rep ,nbCycles,listWrong)

    rep = verif_popular(players, nb_resources, FH, SH)

    print("avant l'algo rep=", rep)


    cpt=0

    while(rep==False and cpt<10):
        #chaque iteration on tester pour bad_agent ou good_agent

        bad_agents = []  # agents holding a bad house (not a first or a second house)
        for p in players:
            if (FH[p.num] != p.bundle[0] and SH[p.num] != p.bundle[0] and GH[p.num] != p.bundle[0]):
                bad_agents.append(p)
                print("bad house for {}".format(p.num))

        print("bad house ",bad_agents)
        good_agents = []
        for p in players:
            if (GH[p.num] == p.bundle[0]):
                good_agents.append(p)
                print("good house for {}".format(p.num))
        print("good house list ", good_agents)



        if( len(bad_agents)!=0):
            #gooodhouseexchange
            print("let me konw we are doing the goodpathExchange")
            nbCycles = 0
            # back = True
            # while (back) :
            rand_bad_agent = random.randint(0, len(bad_agents) - 1)
            # print("RAND = {} , (max = {})".format( rand_bad_agent, len(bad_agents)-1))
            # back = False
            p1 = bad_agents.pop(rand_bad_agent)

            print("selected bad agent p1 {} with item {}".format(p1.num, p1.bundle[0]))

            if (FH[p1.num] != p1.bundle[0] and SH[p1.num] != p1.bundle[0]):  # p1 is still a bad agent
                sec_p1 = SH[p1.num]

                print("second of p1", sec_p1, "agent p1 is ", p1.num)
                p2 = players[house_to_agents[sec_p1]]
                # first_p2 = FH[p2.num]
                first_p2 = GH[p2.num]  # agent p2 get GH
                print("good house of p2", first_p2, "agent p2 is ", p2.num)

                p3 = players[house_to_agents[first_p2]]
                # if(p3==p1):
                #     print("system situation here")
                #
                #     b1 = list(p1.bundle)
                #     b2 = list(p2.bundle)
                #     p1.swap(b1, b2)
                #     p2.swap(b2, b1)

                if (sec_p1 != -1 and p3.num != p1.num and p3.num != p2.num):
                    # print("3 system situation here")
                    b1 = list(p1.bundle)

                    print("b1", b1)
                    b2 = list(p2.bundle)
                    print("b2", b2)

                    b3 = list(p3.bundle)
                    print("b3", b3)

                    # lEch = already_Done[p1.num][p2.num][p3.num]

                    stockState = exchAlreadyDone(lAlloc, classeState.StateAlloc(getAlloc(players, nb_resources)),
                                                 [p1.num, p2.num, p3.num], [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                 nb_resources, 3)

                    if (stockState == None):
                        print("exchange never done")

                        allocSeen = already_seen(lAlloc, getAlloc(players, nb_resources), nb_resources)

                        if allocSeen == None:  # allocation never seen , add without problem to lAllo

                            stateAll = classeState.StateAlloc(getAlloc(players, nb_resources))
                            stateAll.addState(
                                classeState.statExch([p1.num, p2.num, p3.num],
                                                     [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                     0))
                            lAlloc.append(stateAll)
                        else:
                            # print("alloc considérée {}".format(allocSeen))
                            allocSeen.addState(
                                classeState.statExch([p1.num, p2.num, p3.num],
                                                     [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                     nbExch))

                        if display:
                            print(
                                "echange selec : {} donne {} et recoit {},{} donne {} et recoit {}, {} donne {} et recoit {} ".format(
                                    p1.num, b1, b2, p2.num, b2, b3, p3.num, b3, b1))

                        p1.swap(b1, b2)
                        p2.swap(b2, b3)
                        p3.swap(b3, b1)
                        house_to_agents[b1[0]] = p3.num
                        house_to_agents[b2[0]] = p1.num
                        house_to_agents[b3[0]] = p2.num
                        nbExch = nbExch + 1

                        # printCool(already_Done, nb_resources)

                        print(type(b1[0]))

                        print(type(GH[p3.num]))
                        if (FH[p3.num] != b1[0] and SH[p3.num] != b1[0] and (FH[p3.num] == b3[0] or SH[p3.num] == b3[
                            0])):  # p3 is not in the list of bad agents and must be added to the list
                            bad_agents.append(p3)
                        if (FH[p2.num] != b2[0] and SH[p2.num] != b2[
                            0]):  # p2 is in the list of bas agents and must be remove
                            bad_agents.remove(p2)
                        for p in players:
                            if (FH[p.num] != p.bundle[0] and SH[p.num] != p.bundle[0] and GH[p.num] != p.bundle[0]):
                                bad_agents.append(p)

                    else:  # the exchange has already been done
                        # TODO backtrack and find anotre ecxchange

                        print("already DONE {} !".format(stockState))
                        print("old nb Exch {}".format(nbExch))

                        oldNb = nbExch
                        # if nbExch > nbe:
                        nbCycles = nbCycles + 1

                        nbExch = stockState.getNbexch()

                        print("new nb Exch {}".format(nbExch))

                        if nbCycles > 0 or nbExch == oldNb:
                            print("cycle detected")
                            # raise Exception("old nb Exch {} new nb Exch {}, nbCycles = {}".format(oldNb, nbExch, nbCycles))
                            listWrong.append(house_to_agents)
                            print("house_to_vide")
                            return (False, 1, listWrong)
                        # back = True

                        bad_agents.append(p1)
            print("len bad agents {}".format(len(bad_agents)))


        elif(len(good_agents)!=0 and len(bad_agents)==0):
            #we do randompathexchange
            # for p in bad_agents:
            #     print("*****************bad house for {}".format(p.num))
            #
            # for p in players:
            #     print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

            # print("houses to agents {}".format(house_to_agents))
            print("let me konw we are doing the randompathexchange")
            nbCycles = 0
            # back = True
            # while (back) :
            rand_good_agent = random.randint(0, len(good_agents) - 1)
            # print("RAND = {} , (max = {})".format( rand_bad_agent, len(bad_agents)-1))
            # back = False
            p1 = good_agents.pop(rand_good_agent)

            print("selected bad agent p1 {} with item {}".format(p1.num, p1.bundle[0]))

            if (FH[p1.num] != p1.bundle[0] and SH[p1.num] != p1.bundle[0]):  # p1 is still a bad agent
                sec_p1 = SH[p1.num]
                p2 = players[house_to_agents[sec_p1]]
                first_p2 = FH[p2.num]

                p3 = players[house_to_agents[first_p2]]

                if (sec_p1 != -1 and p3.num != p1.num and p3.num != p2.num):
                    b1 = list(p1.bundle)
                    b2 = list(p2.bundle)
                    b3 = list(p3.bundle)

                    # lEch = already_Done[p1.num][p2.num][p3.num]

                    stockState = exchAlreadyDone(lAlloc, classeState.StateAlloc(getAlloc(players, nb_resources)),
                                                 [p1.num, p2.num, p3.num], [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                 nb_resources, 3)

                    if (stockState == None):
                        print("exchange never done")

                        allocSeen = already_seen(lAlloc, getAlloc(players, nb_resources), nb_resources)

                        if allocSeen == None:  # allocation never seen , add without problem to lAllo

                            stateAll = classeState.StateAlloc(getAlloc(players, nb_resources))
                            stateAll.addState(
                                classeState.statExch([p1.num, p2.num, p3.num],
                                                     [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                     0))
                            lAlloc.append(stateAll)
                        else:
                            # print("alloc considérée {}".format(allocSeen))
                            allocSeen.addState(
                                classeState.statExch([p1.num, p2.num, p3.num],
                                                     [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                     nbExch))

                        if display:
                            print(
                                "echange selec : {} donne {} et recoit {},{} donne {} et recoit {}, {} donne {} et recoit {} ".format(
                                    p1.num, b1, b2, p2.num, b2, b3, p3.num, b3, b1))

                        p1.swap(b1, b2)
                        p2.swap(b2, b3)
                        p3.swap(b3, b1)
                        house_to_agents[b1[0]] = p3.num
                        house_to_agents[b2[0]] = p1.num
                        house_to_agents[b3[0]] = p2.num
                        nbExch = nbExch + 1

                        # printCool(already_Done, nb_resources)

                        if (FH[p3.num] != b1[0] and SH[p3.num] != b1[0] and (FH[p3.num] == b3[0] or SH[p3.num] == b3[
                            0])):  # p3 is not in the list of bad agents and must be added to the list
                            good_agents.append(p3)

                        if (FH[p2.num] != b2[0] and SH[p2.num] != b2[
                            0]):  # p2 is in the list of bas agents and must be remove
                            good_agents.remove(p2)

                    else:  # the exchange has already been done
                        # TODO backtrack and find anotre ecxchange

                        print("already DONE {} !".format(stockState))
                        print("old nb Exch {}".format(nbExch))

                        # oldNb  = nbExch
                        # if nbExch > nbe:
                        nbCycles = nbCycles + 1

                        nbExch = stockState.getNbexch()

                        print("new nb Exch {}".format(nbExch))

                        # if nbCycles > 0 or nbExch == oldNb:
                        if nbCycles > 0:
                            print("cycle detected")
                            # raise Exception("old nb Exch {} new nb Exch {}, nbCycles = {}".format(oldNb, nbExch, nbCycles))
                            return (False, 1)
                        # back = True

                        good_agents.append(p1)
            print("len bad agents {}".format(len(good_agents)))


        rep = verif_popular(players, nb_resources, FH, SH)
        print("ssr", house_to_agents)
        cpt+=1
        print("apre cette echange rep=",rep )
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

    if (display):
        print("\n\n--------------------\n ALLOC at the END of the algorithm\n")
        print("ssr", house_to_agents)

        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

        if (nbCycles > 0):
            print("nb Cycles detected : {}".format(nbCycles))


    return (rep, nbCycles)


def main():
    random.seed(time.time())

    init = [[0], [1], [3], [2]]  # initial allocation of Table 4
    # init = [[0], [1],[2],[3],[4]]
    # init = [[0],[3],[1],[2]] # initial allocation of Table 5
    print("Allocation initiale : {}".format(init))
    preferences = [[3, 1, 2, 4], [4, 2, 1, 3], [2, 3, 1, 4], [3, 1, 2, 4]]
    cpt = 0
    for i in range(1):
        rep, nbC= goodhouse_path_to_popular(init, preferences, utility.additive, True)
        if rep:
            cpt += 1

    if rep:
        print("Popular Matching found , nbC = {} ".format(nbC))
    else:
        print("Popular Matching NOT found nbC = {} ".format(nbC))
    if (cpt == 100):
        print("ok")
    else:
        print(cpt)
        #print(listWrong)


    a = transfer(preferences.copy())

    print("ind:", a)



main()


