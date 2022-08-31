# MINIMAL ENVY MATCHING ALGO.
# from Kondratev et al. derived from Abraham et al.

#from housemarkets import allocTools, player, utility
import random

import allocTools, player, utility

# STEP 1 of the algorithm

def match_first(status_agents,status_houses, FH, SH,  FA, SA,  nb_players, nbAlloc=0):

    for i in range(0, nb_players) :
        if status_agents[i] == -1 :
            print("agent : {}, statut {},  FH {} , FA {}".format(i, status_agents[i], FH[i], FA[FH[i]]))
        if status_agents[i] == -1 and FA[FH[i]] == 1:
            status_houses[FH[i]] = i
            status_agents[i] = FH[i]
            FA[FH[i]] = 0
            SA[SH[i]] = SA[SH[i]]  - 1
            nbAlloc = nbAlloc +1




# STEP 2 of the algorithm

def match_second(status_agents, status_houses, FH, SH, FA, SA,  nb_players, nbAlloc=0):
    for i in range(0, nb_players):
        #print("agent : {}, statut {},  SH{} , SA {}".format(i, status_agents[i], SH[i], SA[SH[i]]))
        if status_agents[i] == -1 and SA[SH[i]] == 1:
            status_houses[SH[i]] = i
            status_agents[i] = SH[i]
            FA[FH[i]] = FA[FH[i]] - 1
            SA[SH[i]] = 0
            nbAllloc = nbAlloc +1
            return True
    return False


#STEP 3 of the algorithm

def eliminate_agent(status_agents, FH, SH, FA,  SA, nb_players):

    for i in range(0, nb_players):
        if(status_agents[i] == -1 and  ( FA[FH[i]] >2  or SA[SH[i]] > 2)) :
            status_agents[i] = -2
            FA[FH[i]] = FA[FH[i]] -1
            SA[SH[i]] = SA[SH[i]] -1
            print("REMOVE agent {}".format(i))
            return True
    return False


def eliminate_agentRandom(status_agents, FH, SH, FA,  SA, nb_players):
    pickList=[]
    agentPick=-1
    for i in range(0, nb_players):
        if(status_agents[i] == -1 and  ( FA[FH[i]] >2  or SA[SH[i]] > 2)) :
            pickList.append(i)
    if len(pickList)==0:
        return False
    else:
        agentPickNumber=random.randint(0, len(pickList)-1)
        agentPick=pickList[agentPickNumber]
        print("agentPick", agentPick, "lenPickList", len(pickList))

        if agentPick!=-1:
            status_agents[agentPick] = -2
            FA[FH[agentPick]] = FA[FH[agentPick]] -1
            SA[SH[agentPick]] = SA[SH[agentPick]] -1
            print("REMOVE agent {}".format(agentPick))
            return True
        else:
            return False

def eliminate_agentTry(status_agents, FH, SH, FA,  SA, nb_players,utilities):

    #on doit choisr l'agent qui a plus grande rang pour le second house.

    maxRang=0
    agentPick=-1

    #    preferences = [[4, 3, 2, 1], [3, 4, 2, 1], [1,4, 3, 2], [3, 4, 2, 1]]
    for i in range(0, nb_players):
        if(status_agents[i] == -1 and  ( FA[FH[i]] >2  or SA[SH[i]] > 2)) :
            curRang=utilities[i].index(SH[i])
            print(curRang)
            if maxRang<curRang:
                maxRang=curRang
                agentPick=i
            status_agents[i] = -2
            FA[FH[i]] = FA[FH[i]] -1
            SA[SH[i]] = SA[SH[i]] -1
            print("REMOVE agent {}".format(i))
            return True
    return False


# Apply Kondratev et al. 's algo. "minimal envy matchings"
def mem_matching(nb_resources ,utilities, u, display=False):
    # Initialisation des agents
    players = [player.Player(i, [], utilities[i], u) for i in range(nb_resources)]

    #init FH, SH, FA and SA

    FH = [-1] * nb_resources
    isFH = [False] * nb_resources
    SH = [-1] * nb_resources
    FA =[0] * nb_resources # correspond to the number of first house arcs adjacent to some house in the graph
    SA = [0] * nb_resources # correspond to the number of second house arcs adjacent to some house in the graph
    i = 0
    for p in players :
        m1= p.get_best_item(nb_resources)
       # print("players {} best {} second{}".format(p.num, m1, m2))
        isFH[m1] = True
        FH[p.num] = m1
        FA[m1] = FA[m1] + 1
    for p in players :
        m2 = p.get_best_sec_item(nb_resources, isFH)
        print("m2 : {}".format(m2))
        SH[p.num] = m2
        if(m2 != -1):
            SA[m2] = SA[m2]+1


    #init matched and unmatched agents and houses

    status_agents = [-1] * nb_resources # -2 : agent eliminated, -1 agent not assigned to a house , i >=0 agent  assigned to house i
    status_houses = [-1] * nb_resources # -1 house not assigned, i >= 0 house assigned to agent i

    print("first houses : {} \n second houses {} ".format(FH, SH))
    print("first agents : {} \n second agents {} ".format(FA, SA))

    step = 1
    notEnd = True

    while (notEnd) :

        if step == 1 :
            print("STEP 1")
        #STEP 1
            match_first(status_agents,status_houses, FH, SH, FA, SA, nb_resources)
            step = 2
            if (display):
                print("alloc at the end of STEP 1 {}".format(status_agents))


        elif step == 2  :
            print("STEP 2")
            if (match_second(status_agents,status_houses, FH,  SH, FA, SA, nb_resources)):
                step = 1
            else :
                step = 3
            if (display):
                print("alloc at the end of STEP 2 {}".format(status_agents))

        elif step == 3 :
            print("STEP 3")
            if(eliminate_agentRandom(status_agents, FH, SH, FA, SA, nb_resources )): #on donne le preference pour choisir l'agent pour eliminer.
                step = 1
            else :
                step = 4
            if (display):
                print("alloc at the end of STEP 3 {}".format(status_agents))
        elif step == 4 : # each remaining house has exactly two edges
            print("STEP 4")
            ag_i = -1
            i = 0
            while ag_i == -1 and i < nb_resources :
                if status_agents[i] == -1 :
                    if ag_i == -1 :
                        ag_i = i
                i = i+1


            while ag_i != -1 :
                print("selected agent {}".format(ag_i))
                # match ag_i and her first house
                status_houses[FH[ag_i]] = ag_i
                status_agents[ag_i] = FH[ag_i]
                FA[FH[ag_i]] = FA[FH[ag_i]] -1
                SA[SH[ag_i]] = SA[SH[ag_i]] - 1

                print("first houses : {} \n second houses {} ".format(FH, SH))
                print("first agents : {} \n second agents {} ".format(FA, SA))
                print("status agents : {} \n ".format(status_agents))
                # match ag_j and her first house
                ag_j = -1
                j = 0
                while ag_j  == -1 and j < nb_resources :
                    if j != ag_i and status_agents[j] == -1  and FH[ag_i] == FH[j]:
                        ag_j = j
                    j = j+1

                print("selected second agent {}".format(ag_j))
                status_houses[SH[ag_j]] = ag_j
                status_agents[ag_j] = SH[ag_j]
                print("status agents : {} \n ".format(status_agents))
                FA[FH[ag_j]] = FA[FH[ag_j]] - 1
                SA[SH[ag_j]] = SA[SH[ag_j]] - 1

                ag_i = -1
                # new value for ag_i if necessary
                if(SA[SH[ag_j]] > 0) :
                    i = 0

                    while ag_i == -1 and i < nb_resources:
                        if i != ag_j and status_agents[i] == -1 and SH[i] == SH[ag_j]:
                            ag_i = i
                        i = i + 1
                #print("new value for ag_i {}".format(ag_i))
            step = 5
            if (display):
                print("alloc at the end of STEP 4 {}".format(status_agents))

        else : # step 5 -> Apply again the algorithm with eliminated agents
            print("STEP 5")
            nbFreeHouses = 0
            lFreeHouses =[]

            for i in range (0, nb_resources) :
                if status_agents[i] == -2:
                    status_agents[i] = -1
                if status_houses[i] == -1 :
                    nbFreeHouses = nbFreeHouses +1
                    lFreeHouses.append(i)

                FH[i]= -1
                isFH[i] = False
                SH[i] = -1
                FA[i] = 0
                SA [i] = 0

            print("free houses {}".format(lFreeHouses))
            if(nbFreeHouses == 0) :
                notEnd = False
            else :

                for i in range (0, nb_resources) :
                    if status_agents[i] == -1 :
                        m1= p.get_best_item_restr(lFreeHouses, nbFreeHouses)
                        # print("players {} best {} second{}".format(p.num, m1, m2))
                        isFH[m1] = True
                        FH[i] = m1
                        FA[m1] = FA[m1] + 1
                for i in range (0, nb_resources) :
                    if status_agents[i] == -1:
                        m2 = p.get_best_sec_item_restr(isFH,lFreeHouses, nbFreeHouses)
                        SH[i] = m2
                        SA[m2] = SA[m2]+1
                print("players {} best {} second{}".format(i, m1, m2))
                print("status agents : {} \n ".format(status_agents))
                print("first houses : {} \n second houses {} ".format(FH, SH))
                print("first agents : {} \n second agents {} ".format(FA, SA))
               # print("status agents : {} \n ".format(status_agents))
                step = 1

    # assign houses to players

    for i in range(0, nb_resources) :
        players[i].assign_bundle(list([status_agents[i]]))


    if (display):
        print("ALLOC at the END  of the algorithm\n")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        print("\n\n")

    #ajouter une partie pour calculer Rang MaxMin et Score de Borda

    ScoreBorda=0
    for p in players:
        ScoreBorda+=p.selfutility()
        #print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
    #print(ScoreBorda)

    RangMaxMin=99
    for p in players:
        RangMaxMin=min(RangMaxMin,p.selfutility())

    print(RangMaxMin)
    return ScoreBorda, RangMaxMin


def transfer(preferences):
    list=[]
    for i in range(len(preferences)):

        sorted_nums = sorted(enumerate(preferences[i]), key=lambda x: x[1], reverse=True)
        idx = [i[0]+1 for i in sorted_nums]
        nums = [i[1] for i in sorted_nums]
        list.append(idx)


    return list

def main():
    # init = [[3], [0], [3], [2]]
    # print("Allocation initiale : {}".format(init))
    preferences = [[4,2,1,3],[2,3,1,4],[4,2,3,1],[1,3,2,4]] # exemple of Table 5 , all houses allocated at step 3
    #preferences = [[4, 2, 3, 1], [2, 3, 1, 4], [4, 2, 3, 1], [1, 3, 2, 4]]
    #preferences = [[1, 2, 3, 4], [2,3,4,1], [2,4,3,1], [2, 4,3,1]]
    #preferences= [[4,3,2,1],[4,3,2,1],[4,3,2,1], [1, 3,3,2] ]# one agent allocate at STEP 1, one eliminated at STEP 3, 2 allocated at STEP 4 and then STEP 5 with one agent
    preferences = [[4, 3, 2, 1], [3, 4, 2, 1], [1,4, 3, 2], [3, 4, 2, 1]]
    preferences =[[4,3,2,1],[4,3,2,1],[4,3,2,1],[4,3,1,2]]
    preferences = [[4, 3, 2, 1], [3, 4, 2, 1], [1, 4, 3, 2], [3, 4, 2, 1]]

    preferences= [[4,3,2,1],[4,3,2,1],[4,3,2,1], [3,4,1,2] ]
    #preferences = [[4, 2, 3, 1,5], [4, 3, 2, 1,5], [4, 3, 2, 1,5], [3, 4, 1, 2,5],[3, 4, 1, 2,5]]
    #preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 1, 2]]

    #preferences = [[4, 3, 2, 1], [3, 4, 2, 1], [1, 4, 3, 2], [3, 4, 2, 1]]
    #preferences = [[4, 3, 2, 1], [3, 4, 1, 2], [1, 4, 3, 2], [3, 4, 2, 1]]
    #preferences = [[4, 2, 3, 1, 5], [4, 3, 2, 1, 5], [4, 3, 2, 1, 5], [3, 4, 1, 2, 5], [3, 4, 1, 2, 5]]

    #preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 1, 2]]
    #preferences = [[2, 3, 4, 1], [1, 3, 4, 2], [2, 3, 1, 4], [1, 2, 4, 3]]
    #preferences = [[3, 4, 1, 2], [2, 1, 4, 3], [3, 4, 2, 1], [3, 4, 2, 1]]
    preferences = [[3, 4, 2, 1], [2, 4, 3, 1], [4, 2, 3, 1], [3, 4, 2, 1]]
    preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [3, 4, 1, 2]]
    preferences = [1, 3, 2, 4], [1, 3, 2, 4], [2, 4, 1, 3], [1, 2, 3, 4]

    ScoreBorda,RangMaxMin=mem_matching(4, preferences,utility.additive, True)
    #preferences = [[4, 3, 2, 1], [4, 3, 2, 1], [4, 3, 2, 1], [3, 4, 1, 2]]
    a=transfer(preferences)
    print(a)

    print(ScoreBorda,RangMaxMin)


main()


