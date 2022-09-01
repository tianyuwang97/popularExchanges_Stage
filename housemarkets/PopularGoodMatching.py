import numpy as np
import copy
import random
import time
#from housemarkets import allocTools, player, utility, classeState
import allocTools, player, utility, classeState
def printCool(lEch, n) :
    for i in range (0,n) :
        print("\n")
        for j in range (0,n) :
            print("\n")
            for k in range (0,n) :
                print("{} ".format(lEch[i][j][k]))


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


# Apply Kondratev et al. 's algo. "random path to popular matchings"
def random_path_to_popular(initial, utilities, u, display=False):
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


    nbItem  = len(players)

    #initi FH, SH

    FH = [-1] * nb_resources
    GH = [-1] * nb_resources
    listPre = transfer(utilities)
    print(listPre)
    isFH = [False] * nb_resources
    SH = [-1] * nb_resources
    i = 0
    for p in players :
        m1= p.get_best_item(nb_resources)
        #print("M1:")
        isFH[m1] = True
        FH[p.num] = m1
    for p in players :

        m2 = p.get_best_sec_item(nb_resources, isFH)
        SH[p.num] = m2
    GH = [-1] * nb_resources
    for p in players:
        # print(isFH)

        # print("p.num=",p.num)
        mg = p.get_good_item(nb_resources, isFH, listPre[p.num])
        # mg = p.get_good_item2(nb_resources, isFH,isSH, listPre[p.num])

        # print("mg=", mg)
        GH[p.num] = mg
    print("good house", GH)
    #first part of the algorithm



    print("first houses : {} \n second houses {} ".format(FH, SH))


    for p1  in  players :

        first_p1 = FH[p1.num]
        if(first_p1 != p1.bundle[0]) : # the agent does not hold her first house
            p2 = players[house_to_agents[first_p1]]
            first_p2 = FH[p2.num]
            if(house_to_agents[first_p2] == p1.num  and p1.num != p2.num): # perform a swap between p1 and p2
                b1 = list(p1.bundle)
                b2 = list(p2.bundle)
                if display:
                    print("{} gives {} to {} who gives  {}".format(p1.num, b1, p2.num, b2))
                p1.swap(b1, b2)
                p2.swap(b2, b1)
                house_to_agents[b1[0]] = p2.num
                house_to_agents[b2[0]] = p1.num
                nbExch = nbExch +1

            else :
                p3 = players[house_to_agents[first_p2]] # perform a C3 deal
                if(p3.num != p1.num and p3.num != p2.num):
                    b1 = list(p1.bundle)
                    b2 = list(p2.bundle)
                    b3 = list(p3.bundle)
                    if display:
                        print(
                            "echange selec : {} donne {} et recoit {},{} donne {}et recoit {}, {} donne {} et recoit {} ".format(
                                p1.num, b1, b2, p2.num, b2, b3, p3.num, b3, b1))

                    p1.swap(b1, b2)
                    p2.swap(b2, b3)
                    p3.swap(b3, b1)
                    house_to_agents[b1[0]] = p3.num
                    house_to_agents[b2[0]] = p1.num
                    house_to_agents[b3[0]] = p2.num
                    nbExch = nbExch + 1






    #second part of the algorithm

    bad_agents =[] # agents holding a bad house (not a first or a second house)
    already_Done = [[[[] for k in range(nb_resources)] for j in range(nb_resources)] for i in range(nb_resources)]
    lAlloc = [] # list of the allocation seen and the list of exchanges for each allocation
    lAlloc.append(classeState.StateAlloc(getAlloc(players, nb_resources)))
    nbe = -1

    switch=True #True== popular matching False ==good matching

    print("agents with bad houses:")
    for p in players :
        if(FH[p.num] != p.bundle[0] and SH[p.num] != p.bundle[0]):
            bad_agents.append(p)
            print("bad house for {}".format(p.num))
    good_agents = []
    for p in players:
        if (GH[p.num] == p.bundle[0]):
            good_agents.append(p)
            print("good house for {}".format(p.num))


    print("nb good agent",len(good_agents))
    if (display):
        print("ALLOC after first part of the algorithm\n")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        print("\n\n")

    while((switch==True and len(bad_agents)  != 0 ) or (switch==True and len(good_agents)!=0) or (switch==False and len(good_agents)!=0 ) or (switch==False and len(bad_agents)!=0) ): #and nbExch <= stop : # TODO : the second part of the condition must be revised
    #its the condition for the popular matching but we want the condition for the good exchange is len_goodagent=0

        for p in bad_agents:
            print("*****************bad house for {}".format(p.num))

        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

        #print("houses to agents {}".format(house_to_agents))

        nbCycles = 0
       #  #back = True
       #  #while (back) :
       #  #if len(bad_agents)!=0:
       #  rand_bad_agent = random.randint(0, len(bad_agents)-1)
       # # print("RAND = {} , (max = {})".format( rand_bad_agent, len(bad_agents)-1))
       #  #back = False
       #  p1 = bad_agents.pop(rand_bad_agent)

        print("selected bad agent p1 {} with item {}".format(p1.num,p1.bundle[0]))
        if switch==True:
            print("Swtich is True")

            if len(bad_agents)==0:
                switch=False
                continue
            rand_bad_agent = random.randint(0, len(bad_agents) - 1)
            # print("RAND = {} , (max = {})".format( rand_bad_agent, len(bad_agents)-1))
            # back = False
            p1 = bad_agents.pop(rand_bad_agent)

            print("selected bad agent p1 {} with item {}".format(p1.num, p1.bundle[0]))




            if (FH[p1.num] != p1.bundle[0] and SH[p1.num] != p1.bundle[0]): # p1 is still a bad agent
                sec_p1 = SH[p1.num]
                p2 = players[house_to_agents[sec_p1]]
                first_p2 = FH[p2.num]

                p3 = players[house_to_agents[first_p2]]

                if (sec_p1 != -1 and p3.num != p1.num and p3.num != p2.num):
                    b1 = list(p1.bundle)
                    b2 = list(p2.bundle)
                    b3 = list(p3.bundle)

                    #lEch = already_Done[p1.num][p2.num][p3.num]


                    stockState = exchAlreadyDone(lAlloc, classeState.StateAlloc(getAlloc(players, nb_resources)),[p1.num, p2.num, p3.num],[ p1.bundle[0],p2.bundle[0], p3.bundle[0]],nb_resources,3)

                    if(stockState == None):
                        print("exchange never done")

                        allocSeen = already_seen(lAlloc, getAlloc(players, nb_resources), nb_resources)


                        if allocSeen == None:  # allocation never seen , add without problem to lAllo

                            stateAll = classeState.StateAlloc(getAlloc(players, nb_resources))
                            stateAll.addState(
                                classeState.statExch([p1.num, p2.num, p3.num], [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
                                                     0))
                            lAlloc.append(stateAll)
                        else:
                           # print("alloc considérée {}".format(allocSeen))
                            allocSeen.addState(
                                classeState.statExch([p1.num, p2.num, p3.num], [p1.bundle[0], p2.bundle[0], p3.bundle[0]],
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

                        #printCool(already_Done, nb_resources)



                        if(FH[p3.num] != b1[0] and SH[p3.num] != b1[0] and (FH[p3.num] == b3[0]  or SH[p3.num] == b3[0])): # p3 is not in the list of bad agents and must be added to the list
                            bad_agents.append(p3)

                        if (FH[p2.num] != b2[0] and SH[p2.num] != b2[0]): #p2 is in the list of bas agents and must be remove
                            if p2 in bad_agents:

                                bad_agents.remove(p2)
                        good_agents = []
                        for p in players:
                            if (GH[p.num] == p.bundle[0]):
                                good_agents.append(p)
                                print("good house for {}".format(p.num))
                        switch=False

                    else : # the exchange has already been done
                        #TODO backtrack and find anotre ecxchange

                        print("already DONE {} !".format(stockState))
                        print("old nb Exch {}".format(nbExch))


                        #oldNb  = nbExch
                       # if nbExch > nbe:
                        nbCycles = nbCycles + 1


                        nbExch = stockState.getNbexch()


                        print("new nb Exch {}".format(nbExch))

                        #if nbCycles > 0 or nbExch == oldNb:
                        if nbCycles > 0 :
                            print("cycle detected")
                            #raise Exception("old nb Exch {} new nb Exch {}, nbCycles = {}".format(oldNb, nbExch, nbCycles))
                            return (False, 1)
                        #back = True

                        bad_agents.append(p1)
            print("len bad agents {}".format(len(bad_agents)))
            switch=False
            print("swtich",switch)

        elif switch==False:
            print("Swtich is False")
            print("len_badagent",len(bad_agents))
            print("len goodagent",len(good_agents))

            mode=-1



            # if(len(good_agents)==0):
            #     continue
            #rand_bad_agent = random.randint(0, len(bad_agents) - 1)

            #rand_good_agent= random.randint(0, len(good_agents) - 1)
            # print("RAND = {} , (max = {})".format( rand_bad_agent, len(bad_agents)-1))
            # back = False
            if(len(good_agents)!=0):
                rand_good_agent = random.randint(0, len(good_agents) - 1)
                p1 = good_agents.pop(rand_good_agent)
                mode = 2  # mode second agent is bad


            elif(len(bad_agents)!=0):
                rand_bad_agent = random.randint(0, len(bad_agents) - 1)
                p1 = bad_agents.pop(rand_bad_agent)
                mode = 1  # mode first agent is bad
            else:
                switch=True
                continue


        #if (FH[p1.num] != p1.bundle[0] and SH[p1.num] != p1.bundle[0]):  # p1 is still a bad agent
            sec_p1 = SH[p1.num]

            print("second of p1", sec_p1, "agent p1 is ", p1.num)
            p2 = players[house_to_agents[sec_p1]]
            # first_p2 = FH[p2.num]
            first_p2 = GH[p2.num]  # agent p2 get GH
            print("good house of p2", first_p2, "agent p2 is ", p2.num)
            p3 = players[house_to_agents[first_p2]]


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



                    if mode==1:
                        if (FH[p3.num] != b1[0] and SH[p3.num] != b1[0] and (FH[p3.num] == b3[0] or SH[p3.num] == b3[
                            0])):  # p3 is not in the list of bad agents and must be added to the list
                            bad_agents.append(p3)

                        if (FH[p2.num] != b2[0] and SH[p2.num] != b2[
                            0]):  # p2 is in the list of bas agents and must be remove
                            if p2 in bad_agents:
                                bad_agents.remove(p2)
                        for p in players:
                            if (GH[p.num] == p.bundle[0]):
                                good_agents.append(p)
                        print("good_agent",good_agents)
                    elif mode==2:
                        if (FH[p3.num] != b1[0] and SH[p3.num] != b1[0] and (FH[p3.num] == b3[0] or SH[p3.num] == b3[
                            0])):  # p3 is not in the list of bad agents and must be added to the list
                            bad_agents.append(p3)
                        if (FH[p2.num] != b2[0] and SH[p2.num] != b2[
                            0]):  # p2 is in the list of bas agents and must be remove
                            if p2 in good_agents:
                                good_agents.remove(p2)
                        for p in players:
                            if (GH[p.num] == p.bundle[0]):
                                good_agents.append(p)
                        print("good_agent",good_agents)


                    switch = True
                    print("swtich is ",switch)
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
            else:
                print("here")
            print("len bad agents {}".format(len(bad_agents)))
            print("len good agents {}".format(len(good_agents)))
            print("mode",mode)
            switch = True
            print("good excahnege swtich ",switch)




    if(display) :
        print("\n\n--------------------\n ALLOC at the END of the algorithm\n")
        print("ss", house_to_agents)


        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

        if(nbCycles > 0) :
            print("nb Cycles detected : {}".format(nbCycles) )

        else:
            print ("NO cycles detected ")

    if(len(bad_agents) == 0):
        rep = True
    else :
        rep =False


    #if(rep == verif_popular(players, nb_resources,FH, SH)):
    #    print("verif OK")
    #else :
    #    print ("ERREUR VERIF POPULAR")

    return (rep ,nbCycles)





# while((switch==True and len_badagent!=0) or (switch==False and len_goodagent!=0)):
#     if swtich==True:
#         popular exchange
#         siwtch ==False
#         continue
#         if agent 2 has good agent
#             switch=True
#
#     elif swtich ==False:
#         goodexchange
#         swtich==True
#         continue
#         if len_badagent==0:
#             switch =False












#test if the allocation is popular : each agent gets her first or second item
# USE : house-markets where preferences are defined as borda scores
def verif_popular(players, nbItems, FH, SH ):
    for p in players :
        if(p.bundle[0] != FH[p.num] and p.bundle[0] !=SH[p.num]):
            return False
    return True

def transfer(preferences):
    list=[]
    for i in range(len(preferences)):
        sorted_nums = sorted(enumerate(preferences[i]), key=lambda x: x[1], reverse=True)
        idx = [i[0]+1 for i in sorted_nums]
        nums = [i[1] for i in sorted_nums]
        list.append(idx)


    return list





def main():
     random.seed(time.time())

     init = [[0],[0],[1],[3]] # initial allocation of Table 4
     #init = [[0], [1],[2],[3],[4]]
     #init = [[0],[3],[1],[2]] # initial allocation of Table 5
     print("Allocation initiale : {}".format(init))

     #Rpreferences = utility.generate_borda_diff(4, 4)
     #print(preferences)
     #preferences = [[2, 1, 3, 4], [2, 1, 4, 3], [3, 1, 4, 2], [3, 1, 2, 4]] #exemple of Table 5 and Table 4
     #preferences =  [[2, 1, 3, 4], [2, 1, 4, 3], [3, 2, 1, 4], [3, 1, 2, 4]]
     #preferences=[[2, 4, 5, 3, 1], [3, 2, 4, 1, 5], [4, 2, 3, 1, 5], [3, 2, 4, 1, 5], [4, 5, 2, 3, 1]]
     #preferences = [[1, 2, 3, 4, 5], [2, 1, 3, 4, 5], [3, 2, 1, 4, 5], [4, 2, 3, 1, 5], [5, 2, 3, 4, 1]]
     #preferences = [[1, 2, 3, 4], [2, 1, 3, 4], [3, 2, 1, 4], [4, 2, 3, 1]]
     preferences=[[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]
     preferences = [[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]
     preferences = [[2, 3, 1, 4], [3, 2, 1, 4], [2, 4, 3, 1], [3, 4, 2, 1]]
     preferences = [[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]
     #edcba,edcab,edabc,eacbd,adcbe
     #test=[1,2]






     #preferences = [[5,4,3,2,1], [4,5,3,2,1], [3,4,5,2,1], [2,4,3,5,1], [1,4,3,2,5]]



     #preferences = [[1, 2, 3, 4], [2, 1, 3, 4], [3, 2, 1, 4], [4, 2, 3, 1]]

     #preferences = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
     #preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [1, 3, 3, 2]]
     #preferences = [[4, 3, 2, 1], [3, 2, 1, 4], [2, 1, 4, 3], [1, 4, 3, 2]]
     #preferences = [ [3,2,1,4], [4,3,1,4], [3,2,4,1],[1,2,3,4]]
     #preferences = [[3, 4, 1, 2], [3, 4, 2, 1], [3, 4, 1, 2], [2, 4, 3, 1]]
     preferences = [[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

     preferences = [[4, 3, 1, 2], [4, 3, 2, 1], [4, 3, 1, 2], [4, 1, 2, 3]] #non populaire

     preferences = [[4, 2, 1, 3], [4, 1, 2, 3], [1, 3, 2, 4], [4, 3, 1, 2]]

     preferences = [[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

     #preferences = [[1, 3, 4, 2], [4, 3, 2, 1], [4, 3, 1, 2], [4, 1, 2, 3]]

     preferences = [[3, 4, 1, 2], [3, 4, 2, 1], [3, 4, 1, 2], [2, 4, 3, 1]]
     preferences = [[1, 2, 3, 4], [3, 2, 4, 1], [3, 2, 4, 1], [1, 3, 4, 2]]

     preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [1, 3, 3, 2]]

     preferences = [[3, 1, 2, 4], [4, 2, 1, 3], [2, 3, 1, 4], [3, 1, 2, 4]]
     preferences = [[3, 1, 2, 4], [4, 2, 1, 3], [2, 3, 1, 4], [3, 1, 2, 4]]
     #init = [[0], [1], [2], [3]]  # initial allocation of Table 4  #on peut trouve le nombre est 13
     init = [[1], [2], [3], [0]]  #on peut trouver le nombre est 14
     preferences = [[4, 3, 2, 1], [4, 2, 3, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

     # preferences = [[4, 3, 1, 2], [4, 3, 2, 1], [4, 3, 1, 2], [4, 1, 2, 3]]  #instance pour trouver true ou false cycle.
     #
     # preferences = [[4,1,3,2], [4,3,1,2], [4,3,1,2],[4, 1, 3, 2]]

     preferences =[[4,2,1,3],[2,3,1,4],[4,2,3,1],[1,3,2,4]]
     preferences = [[4, 2, 1, 3], [2, 3, 1, 4], [4, 2, 3, 1], [1, 3, 2, 4]]
     preferences = [[1, 3, 4, 2], [4, 3, 2, 1], [4, 3, 1, 2], [4, 1, 2, 3]]
     preferences = [[2, 1, 3, 4], [2, 1, 4, 3], [3, 1, 4, 2], [3, 1, 2, 4]]
     preferences = [[4, 2, 1, 3], [2, 3, 1, 4], [4, 2, 3, 1], [1, 3, 2, 4]]  # exemple of Table 5 and Table 4
     rep , nbC =random_path_to_popular(init, preferences,utility.additive, True)
     if rep :
         print("Popular Matching found , nbC = {} ".format(nbC))
     else :
         print("Popular Matching NOT found nbC = {} ".format(nbC))

    # init2 = [[0], [1], [2]]  # initial allocation of Table 5
     #print("Allocation initiale : {}".format(init))
     #preferences2 = [[3, 2, 1], [3, 2, 1], [3, 2, 1]]  # exemple of Table 5 and Table 4
     #rep2, nbC = random_path_to_popular(init2, preferences2, utility.additive, True)
     #if rep2:
     #   print("Popular Matching found , nbC = {} ".format(nbC))
     #else:
     #    print("Popular Matching NOT found nbC = {} ".format(nbC))


     test = [4, 1, 5, 2, 9, 6, 8, 7]


     a = transfer(preferences)

     print("ind:",a)
        #print("nums:",b)
main()
