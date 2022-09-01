
import random

import allocTools, player, utility
import numpy as np
def test(nb_resources ,utilities, u, display=False):

    # print(nb_resources)
    # print(utilities)
    # print(u)

    listeSB=transfer(utilities)
    print(listeSB)


    SB=len(utilities[0])-getScoreBorda(listeSB,0,1)

    print("number of SB is ",SB)

    #step 0 need to make a first M


    round=1



    M = []

    arcRound = np.zeros((len(utilities), len(utilities)), dtype=list)

    for i in range(len(utilities)):
        for j in range(len(utilities)):
            arcRound[i][j] = [i + 1, -(listeSB[i][j])]
    print("long len(utilities)",len(utilities))


    while (round!=len(utilities)) and (len(M)<len(utilities)):
        agent=[]
        for i in range(len(utilities)):
            agent.append(i + 1)
        print(agent)

        ressource = []

        for i in range(len(utilities)):
            ressource.append(-(i + 1))
        print(ressource)

        #partie 3 comment on fait le Mi (par changer le valeur de round -1
        cpt=round
        Mstore=M
        print("i want to see my Mstore here is right or not ",Mstore)
        print("that is round ",round )
        M = []

        print("now the liste Score Borda is ", listeSB)
        print("cpt is ",cpt)
        # for i in range(len(arcRound)):
        #     print(arcRound[:, round][i])
        while (cpt - 1 >= 0):
            for i in range(len(arcRound)):
                    if arcRound[:, cpt-1][i][0]!=0 and arcRound[:, cpt-1][i][1]!=0 :  #quand on supprime les edges , on fait la position pour l'edge a 0
                        if arcRound[:, cpt-1][i][1] in ressource and arcRound[:,cpt-1][i][0] in agent:
                            M.append([arcRound[:, cpt-1][i][0],arcRound[:, cpt-1][i][1]])
                            print("liste agent ",agent)
                            print("liste ressource",ressource)
                            #print(agent[i+1])
                            print("le agent on va supprimer ",arcRound[:, cpt-1][i][0])
                            print("le ressource on va supprimer",arcRound[:,cpt-1][i][1])
                            agent.remove(arcRound[:, cpt-1][i][0])
                            ressource.remove(arcRound[:, cpt-1][i][1])
                            #print(M)
            cpt-=1

        if(len(M)==len(utilities)-1):
            M.append([agent.pop(), ressource.pop()])

        resMstore = calculeSB(listeSB, Mstore)
        resM=calculeSB(listeSB,M)


        if(len(Mstore)==len(M) and resM<resMstore):
            M=Mstore



        print(arcRound)
        print(arcRound[:, 0][2][1])
        print("agent:", agent)
        print("ressource", ressource)
        print("M apres chaque iteration",M)
        print("ressource",ressource)
        # part 1 divide all the agent and ressorce to 3 parties
        destList=set([])
        startList=set([])
        # for i in range(len(arcRound1)):
        #     destList.add(arcRound1[i][1])
        #     startList.add(arcRound1[i][0])
        for i in range(len(arcRound)):
            destList.add(arcRound[:, round-1][i][1])
            startList.add(arcRound[:, round-1][i][0])

        print("destList",destList)
        print("startList", startList)
        E = []
        O = []
        U = []
        cpt = 0

        print("before we start the list agent is ", agent)
        #while len(agent) !=0:
        nbAgent=0
        while nbAgent<len(agent):
            #print("i am here")

            for i in range(len(arcRound)):
                # print("lets bug here i egale ", i)
                # print("lets bug here agent =", agent)
                if agent:
                    if agent[0]==arcRound[:, round-1][i][0]:
                        cur=arcRound[:, round-1][i][1]
                        debut=agent[0]
                        E.append(agent[0])
                        agent.remove(agent[0])
                        O.append(cur)

                        cpt=1

                        while cur in destList:
                            for i in range(len(arcRound)):
                                if cur==arcRound[:, round-1][i][1] and arcRound[:, round-1][i][0]!=debut:
                                    cur=arcRound[:, round-1][i][0]
                                    if cpt%2==0:
                                        O.append(cur)
                                    else:
                                        E.append(cur)
            nbAgent+=1
        while (len(ressource)!=0):
            E.append(ressource[0])
            ressource.remove(ressource[0])
            #for i in range(len(arcRound1)):
                #print("here")


                # if ressource[0]==arcRound1[i][1]:
                #
                #     print("here")
                #     cur=arcRound1[i][0]
                #     debut=ressource[0]
                #     E.append(ressource[0])
                #     ressource.remove(ressource[0])
                #     O.append(cur)

            #arcRound[:, round - 1][i][0]

        arcRoundCur=[]
        for i in range(len(arcRound)):
                arcRoundCur.append([arcRound[:, round - 1][i][0],arcRound[:, round - 1][i][1]])
        for i in range(len(arcRoundCur)):
            if arcRoundCur.count(arcRound[:, round - 1][i][0])==1 and arcRoundCur.count(arcRound[:, round - 1][i][0])==1 :
                U.append(arcRoundCur[i][0])
                U.append(arcRoundCur[i][1])

        print("E",E)
        print("O",O)
        print("U",U)

        #part2 Deleteall   OiOi and  OiUi edges  from  Gi′

        #print(arcRound[:, round][0][1])

        # for i in range(len(O)):
        #     print(arcRound[:, round][i][1])

        for i in range(len(O)):
            print("i am here ")
            for j in range(len(arcRound)):
                if O[i] == arcRound[:, round][j][1] : #on doit supprimer les edges OO plus un niveux
                    print("but i am not here")
                    arcRound[:, round][j][0]=0
                if O[i] == arcRound[:, round][j][0]: #on doit supprimer les edges OO plus un niveux
                    arcRound[:, round][j][1]=0
        for i in range(len(U)):
            if U[i] == arcRound[:, round][i][1] and arcRound[:, round][i][0] in O: #on doit supprimer les edges OO plus un niveux
                listeSB[round][i]=0
            if U[i] == arcRound[:, round][i][0] and arcRound[:, round][i][1] in O:  # on doit supprimer les edges OO plus un niveux
                listeSB[round][i] = 0
        print("arcRound apres on fait supprision")
        print(arcRound)

        round+=1

    agentLast = []
    for i in range(len(utilities)):
        agentLast.append(i + 1)
    print(agentLast)

    ressourceLast = []

    for i in range(len(utilities)):
        ressourceLast.append(-(i + 1))
    print(ressourceLast)
    if len(M)!=len(utilities):
        print("yes i am here")
        for i in range(len(M)):
            agentLast.remove(M[i][0])
            ressourceLast.remove(M[i][1])
        print("agentLast",agentLast)
        print("ressourceLast",ressourceLast)
        while(len(M)!=len(utilities)):
            M.append([agentLast.pop(),ressourceLast.pop()])
    print("the final M is",M)
    print(listeSB)
    #print(listeSB[0])
    # sum=0
    # for i in range(len(M)):
    #     print("agent",M[i][0])
    #     print("ressource",M[i][1])
    #     print("socre SB",(len(utilities)-listeSB[M[i][0]-1].index(-(M[i][1]))))
    #     sum+=(len(utilities)-listeSB[M[i][0]-1].index(-(M[i][1])))
    #
    # print(sum)



    res=calculeSB(listeSB,M)

    print("hi here", M)
    print("score de borda ",res)
    OK=False
    if(len(M)==len(utilities)):
        OK=True

    return res,OK


def calculeSB(listeSB,M):
    sum = 0
    for i in range(len(M)):
        print("agent", M[i][0])
        print("ressource", M[i][1])
        print("socre SB", (len(listeSB) - listeSB[M[i][0] - 1].index(-(M[i][1]))))
        sum += (len(listeSB) - listeSB[M[i][0] - 1].index(-(M[i][1])))

    return sum













def transfer(preferences):
    list=[]
    for i in range(len(preferences)):

        sorted_nums = sorted(enumerate(preferences[i]), key=lambda x: x[1], reverse=True)
        idx = [i[0]+1 for i in sorted_nums]
        nums = [i[1] for i in sorted_nums]
        list.append(idx)


    return list

def getScoreBorda(listSB,agentNb,objet):

    res=listSB[agentNb].index(objet)
    return res


def main():
    # init = [[3], [0], [3], [2]]
    # print("Allocation initiale : {}".format(init))
    preferences = [[4,2,1,3],[2,3,1,4],[4,2,3,1],[1,3,2,4]] # exemple of Table 5 , all houses allocated at step 3

    #preferences = [[1, 2, 4, 3], [2, 3, 4, 1], [4, 2, 3, 1], [1, 3, 2, 4]]
    #preferences = [[4, 3, 2, 1], [3, 4, 2, 1], [1, 4, 3, 2], [3, 4, 2, 1]]

    preferences = [[3, 4, 1, 2], [3, 2, 4, 1], [1, 4, 3, 2], [3, 4, 2, 1]]
    preferences=[[1, 4, 2, 3], [1, 4, 3, 2], [1, 3, 4, 2], [1, 2, 4, 3]]
    preferences=[[4, 2, 3, 1], [1, 4, 2, 3], [4, 3, 1, 2], [3, 1, 2, 4]]



    preferences=[[4,2,1,3],[2,3,1,4],[4,2,3,1],[3,1,4,2]]

    preferences = [[4, 2, 3, 1], [2, 3, 1, 4], [2, 1, 4, 3], [4, 1, 3, 2]]

    listSB=transfer(preferences)

    M=test(4, preferences,utility.additive, True)
    print(listSB)
    print(M)



main()
