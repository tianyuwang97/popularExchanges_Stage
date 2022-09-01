# POPULAR MATCHINGS
#  from Abraham et al.
#
import allocTools, player, utility

#import  player, utility

def match_first(status_agents,status_houses, FH, SH,  FA, SA,  nb_players):
    nbAlloc = 0
    for i in range(0, nb_players) :
        if status_agents[i] == -1 :
            print("agent : {}, statut {},  FH {} , FA {}".format(i, status_agents[i], FH[i], FA[FH[i]]))
        if status_agents[i] == -1 and FA[FH[i]] == 1:
            status_houses[FH[i]] = i
            status_agents[i] = FH[i]
            FA[FH[i]] = 0
            SA[SH[i]] = SA[SH[i]]  - 1
            nbAlloc = nbAlloc +1
    return nbAlloc




# STEP 2 of the algorithm

def match_second(status_agents, status_houses, FH, SH, FA, SA,  nb_players):
    for i in range(0, nb_players):
        print("agent : {}, statut {},  SH{} , SA {}".format(i, status_agents[i], SH[i], SA[SH[i]]))
        if status_agents[i] == -1 and SA[SH[i]] == 1:
            status_houses[SH[i]] = i
            status_agents[i] = SH[i]
            FA[FH[i]] = FA[FH[i]] - 1
            SA[SH[i]] = 0

            return True
    return False


def assign_and_print(status_agents, players, nb_resources):
    print("test")
    for i in range(0, nb_resources):

        players[i].assign_bundle(list([status_agents[i]]))

    print(status_agents)
    print("ALLOC at the END  of the algorithm\n")
    for p in players:
        print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
    print("\n\n")



def popular_matching(nb_resources ,utilities, u, display=False):
    # Initialisation des agents
    players = [player.Player(i, [], utilities[i], u) for i in range(nb_resources)]
    nbAlloc = 0
    #init FH, SH, FA and SA

    FH = [-1] * nb_resources
    isFH = [False] * nb_resources
    SH = [-1] * nb_resources
    FA =[0] * nb_resources # correspond to the number of first house arcs adjacent to some house in the graph
    SA = [0] * nb_resources # correspond to the number of second house arcs adjacent to some house in the graph
    i = 0
    for p in players :
        m1= p.get_best_item(nb_resources)
        #print("players {} best {} second{}".format(p.num, m1, m2))
        isFH[m1] = True
        FH[p.num] = m1
        FA[m1] = FA[m1] + 1
    for p in players :
        m2 = p.get_best_sec_item(nb_resources, isFH)

        SH[p.num] = m2
        if(m2 != -1):
            SA[m2] = SA[m2]+1


    #init matched and unmatched agents and houses

    status_agents = [-1] * nb_resources # -2 : agent eliminated, -1 agent not assigned to a house , i >=0 agent  assigned to house i
    status_houses = [-1] * nb_resources # -1 house not assigned, i >= 0 house assigned to agent i


    step = 1
    notEnd = True

    while (notEnd) :

        if step == 1 :

        #STEP 1
            nbA =match_first(status_agents,status_houses, FH, SH, FA, SA, nb_resources)
            nbAlloc = nbAlloc + nbA
            step = 2
            if (display):
                print("alloc at the end of STEP 1 {}".format(status_agents))

            if(nbAlloc == nb_resources):
                assign_and_print(status_agents, players, nb_resources)
                return True

        elif step == 2  :

            if (match_second(status_agents,status_houses, FH,  SH, FA, SA, nb_resources)):
                step = 1
                nbAlloc = nbAlloc +1
                if (nbAlloc == nb_resources):
                    assign_and_print(status_agents, players, nb_resources)
                    return True
            else :
                 step = 3

            if (display):
                print("alloc at the end of STEP 2 {}".format(status_agents))
        elif step == 3 : # each remaining house has exactly two edges
            print("step 3 ")
            for i in range(0,nb_resources) :
                if(SA[i] + FA[i] > 2) :
                    assign_and_print(status_agents, players, nb_resources)
                    return False
            print("suite step 3")


            ag_i = -1
            i = 0
            while ag_i == -1 and i < nb_resources :
                if status_agents[i] == -1 :
                    if ag_i == -1 :
                        ag_i = i
                i = i+1


            while ag_i != -1 :

                # match ag_i and her first house
                status_houses[FH[ag_i]] = ag_i
                status_agents[ag_i] = FH[ag_i]
                FA[FH[ag_i]] = FA[FH[ag_i]] -1
                SA[SH[ag_i]] = SA[SH[ag_i]] - 1

                nbAlloc = nbAlloc +1
                # match ag_j and her second  house
                ag_j = -1
                j = 0
                while ag_j  == -1 and j < nb_resources :
                    if j != ag_i and status_agents[j] == -1  and FH[ag_i] == FH[j]:
                        ag_j = j
                    j = j+1

                status_houses[SH[ag_j]] = ag_j
                status_agents[ag_j] = SH[ag_j]

                FA[FH[ag_j]] = FA[FH[ag_j]] - 1
                SA[SH[ag_j]] = SA[SH[ag_j]] - 1
                nbAlloc = nbAlloc + 1
                ag_i = -1
                # new value for ag_i if necessary
                if(SA[SH[ag_j]] > 0) :
                    i = 0

                    while ag_i == -1 and i < nb_resources:
                        if i != ag_j and status_agents[i] == -1 and SH[i] == SH[ag_j]:
                            ag_i = i
                        i = i + 1
                else :
                    ag_i = -1
                    i = 0
                    while ag_i == -1 and i < nb_resources:
                        if status_agents[i] == -1:
                            if ag_i == -1:
                                ag_i = i
                        i = i + 1


            if(nbAlloc == nb_resources) :
                assign_and_print(status_agents, players, nb_resources)
                return True
            else :
                assign_and_print(status_agents, players, nb_resources)
                return False

                print("new value for ag_i {}".format(ag_i))
def main():

    init = [[1],[2],[3],[0]]
    #init = [[2], [1], [4], [3]]

    a=utility.additive
    print(a)

    print("Allocation initiale : {}".format(init))
    preferences = [[4,2,1,3],[2,3,1,4],[4,2,3,1],[1,3,2,4]] # exemple Tab 5 popular matching exists
    #preferences = [[4, 3, 2, 1], [3, 2, 1, 4], [2, 1, 4, 3], [1, 4, 3, 2]] # Popular matching obtained at step 1
    #preferences =  [[4, 1, 3, 2], [4, 2, 1, 3], [2, 3, 4, 1], [2, 3, 4, 1]]
    #preferences = [[1, 2, 3, 4], [2,3,4,1], [2,4,3,1], [2, 4,3,1]]
    #preferences = [[4, 3, 2, 1], [1, 4, 3, 2], [2, 3, 4, 1], [3, 2, 1, 4]]
    #preferences= [[4,3,2,1],[4,3,2,1],[4,3,2,1], [1, 3,3,2] ]# NO Popular Matching
    rep = popular_matching(4, preferences,utility.additive, True)



    if rep :
        print("Popular Matching found")
    else :
        print("Popular Matching NOT found")

main()