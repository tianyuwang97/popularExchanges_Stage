import sys
import random
import time
import sys
import itertools
import numpy as np



sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import popularMatching, randomPathPop, utility, allocTools
import os
# from tests import testInstance

import testInstance

sys.path.insert(0, "..")


def test_random_path(nbTests, f, nb_player, listPreferenceAvecCycle, listPreferenceSansCycle,max):
    nbDone = 0
    nbPopFound = 0
    nbInstCycle = 0
    propPopular = 0.0
    propNotPopular = 0.0
    nbNotPopFound = 0.0
    nbInstCycleNotProp = 0.0
    j = 0
    l=0
    initTime = time.time()
    nb_resources = nb_player

    # allocs = allocTools.all_even_sized_alloc(nb_resources, 1)
    # print("Nombre d'allocations differentes : {}".format(len(allocs)))

    while nbDone < nbTests:

        # build an instance
        # print("len allocs {}".format(len(allocs)))
        init = allocTools.generateAlloc(nb_resources)
        #print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player, nb_resources)
        print("Preferences = ", preferences)

        # check if there is a popular matching for this instance

        rep = popularMatching.popular_matching(nb_resources, preferences, f, True)

        # if there is a popular matching, run "random path to popular matching"
        # check if a cycle is detected and  that a popular matching is reached

        if rep:
            #break
            #print("un popular matching existe")
            nbDone = nbDone + 1
            listPreferenceSansCycle[nb_player][l]=preferences.copy()
            l+=1
            #propPopular = propPopular + 1
            #repRand, nbC = randomPathPop.random_path_to_popular(init, preferences, f, True)
            #if repRand:
                #nbPopFound = nbPopFound + 1
            #if nbC > 0:
                #nbInstCycle = nbInstCycle + 1
        else:
            #print("Abraham : no popular")
            nbDone = nbDone + 1
            print("Preference pour tester ",preferences)
            # print("apres transfer:")
            # a=transfer(preferences.copy())
            # print(a)

            listPreferenceAvecCycle[nb_player][j] = preferences.copy()

            propNotPopular = propNotPopular + 1
            #repRand, nbC = randomPathPop.random_path_to_popular(init, preferences, f, True)
            #print("nbC = {}".format(nbC))
            j += 1

            #if repRand:
                #nbNotPopFound = nbNotPopFound + 1
                #raise ("Allocation non prop non trouvée comme telle")
            #if nbC > 0:
                #print("increment")
                #nbInstCycleNotProp = nbInstCycleNotProp + 1
                #print(nbInstCycleNotProp)
            #elif nbC == 0:
                #raise Exception(" pas populaire et pas de cycles")
            #print("pas de populaire pouΩ cette instance, skip")
            # raise Exception("pas pop")

    # print(
    #     "nbInstances {} / nbPopFound {} /  nb Pop Instances with cycles {} / nbNOTProp {} / nbNotFound {} / nonPropWithCycles {}".format(
    #         nbDone, nbPopFound, nbInstCycle, propNotPopular, nbNotPopFound, nbInstCycleNotProp))
    # print(" /// propPop {} / propNotPop {}".format(propPopular / (propPopular + propNotPopular),
    #                                                propNotPopular / (propPopular + propNotPopular)))
    if (propNotPopular == 0):
        propCycles = 1
    else:
        propCycles = nbInstCycleNotProp / propNotPopular
    #return (nbDone, nbPopFound, nbInstCycle, propPopular / (propPopular + propNotPopular),
            #propNotPopular / (propPopular + propNotPopular), nbNotPopFound, propCycles)
    #return 0



def transfer(preferences):
    listx = []
    for i in range(len(preferences)):
        sorted_nums = sorted(enumerate(preferences[i]), key=lambda x: x[1], reverse=True)
        idx = [i[0] + 1 for i in sorted_nums]
        nums = [i[1] for i in sorted_nums]
        listx.append(idx)

    return listx





def transferBordaToPreference(listPreferenceAvecCycle,nbTests):

    listx = []
    for i in range(max):
        for j in range(nbTests):
            # print(listPreferenceAvecCycle[i][j])
            x = transfer(listPreferenceAvecCycle[i][j])
            a = str(x)
            if (a != "[[1]]"):
                #print(a)
                listx.append(a)
    return listx



def transferFromStrToInt(listx):
    n = 0
    m = 0
    res = np.zeros((len(listx), max - 1, max - 1))

    for i in range(len(listx)):

        # print("**********")
        for j in range(len(listx[i])):
            if listx[i][j].isdigit():
                a = int(listx[i][j])
                if (m == max-1):
                    n += 1
                    m = 0
                # print("n=",n)
                # print("m=",m)
                #print(a)
                if (n == max-1):
                    n = 0
                res[i][n][m] = a
                # print("test")
                m += 1

    print(res)
    return res


def com(n):
    res = []
    t_list = []
    for i in range(1, n + 1):
        t_list.append(i)
    for i in itertools.permutations(t_list, n - 1):
        res.append(i)

    return res


def testCondition(res):
    condition1 = False
    # ok=False  #boolean pour tester la condition1

    ok = []
    n = len(res[0][0])
    comb = com(n)

    listrecord = []
    for i in range(len(comb)):
        pivot = list(comb[i])
        for j in range(len(res)):
            stock=False
            cptC1=0
            for m in range(len(res[j])):
                for x in range(2):
                    for y in range(max-3):
                        if(x+1!=y+2):
                            if((pivot[0] == res[j][m][0] and pivot[1] == res[j][m][x+1] and pivot[2] == res[j][m][y+2])):
                                cptC1+=1

            #if (cptC1 >= 3 ):
            if (cptC1 >= 3 ):
                # print("********bingo,c'est le ",j+1," eme allocation on utilise le combo ",pivot)

                ok.append(j)

                stock=True

            if(stock):

                listrecord.append(res[j])

                #print(listrecord)

    ok2 = []
    # toutes les elements de la deuxieme ligne sont pareils
    val = 0
    listrecord2 = []
    for i in range(len(res)):
        cpt = 0
        val = res[i][0][1]
        condition2 = True
        for j in range(len(res[i])):
            # print(len(res[i]))
            # print(j)
            if val != res[i][j][1]:
                condition2 = False

            val = res[i][j][1]

        # val2list=[]

        #         condition3=False
        #         for j in range(len(res[i])):

        #             val2=res[i][j][0]
        #             val2list.append(val2)

        #             a=set(val2list)
        #             print(a)
        #             if(len(a)==len(res[0][0])-2):  # si FH equal n-2
        #                 print(a)
        #                 condition3=True
        #             else:
        #                 condition3=False
        #             val2list=[]

        # if(condition2==True and condition3==True):
        condition3 = False
        vala = res[i][j][0]
        a = 0
        b = 0
        if (condition2 == True):
            for j in range(len(res[i])):

                if (res[i][j][0] == vala):

                    a += 1
                else:
                    b += 1
            if (a==2 and b==2):
            #if ((a == 3 and b == 2) or (a==2 and b==3)):  #pour n=5
                condition3 = True
        # print("hey condition2: ",condition2,"condition3:",condition3)
        if (condition3 == True and condition2 == True):
            ok2.append(condition2)
            listrecord2.append(i)
        else:
            ok2.append(False)

    ok3 = []  # toutes les elements de la 3eme ligne et 1eme ligne sont pareils
    val = 0

    for i in range(len(res)):
        cpt = 0
        val = res[i][0][0]
        condition4 = True
        for j in range(len(res[i])):  # 1eme ligne
            # print(len(res[i]))
            # print(j)
            if val != res[i][j][0]:
                condition4 = False

            val = res[i][j][0]

        val = res[i][0][2]
        for j in range(len(res[i])):  # 3eme ligne
            # print(len(res[i]))
            # print(j)
            if val != res[i][j][2]:
                condition4 = False

            val = res[i][j][2]
        condition5 = False
        vala = res[i][j][1]
        a = 0
        b = 0
        if (condition4 == True):
            for j in range(len(res[i])):

                if (res[i][j][1] == vala):

                    a += 1
                else:
                    b += 1
            if (a == 2 and b == 2):
                condition5 = True
        if (condition4 == True and condition5 == True):
            ok3.append(condition4)
            # listrecord2.append(i)
        else:
            ok3.append(False)

    OK = set(ok)
    # if(len(OK)==1):
    OK2 = set(ok2)
    OK3 = set(ok3)

    #print(listrecord)
    return len(OK), ok2, listrecord, listrecord2, ok3, OK
    # else:
    # return "haha",ok2






def main():
    random.seed(time.time())
    global max
    max = 8
    nbTests = 100
    listRes = [None] * max
    global listPreferenceAvecCycle
    listPreferenceAvecCycle = [[" " for i in range(nbTests)] for j in range(max)]

    global listPreferenceSansCycle
    listPreferenceSansCycle = [[" " for i in range(nbTests)] for j in range(max)]

    # listPreferenceAvecCycleAvantTransfer=[[" " for i in range (1000)] for j in range(max)]

    # print(listPreferenceAvecCycle)
    for i in range(max-1, max):
        res = test_random_path(nbTests, utility.additive, i, listPreferenceAvecCycle,listPreferenceSansCycle, max)
        listRes[i] = res
        if (i % 100 == 0):
            print("{}".format(i))

    #print("listPreferenceAvecCycle",listPreferenceAvecCycle)

    x = transferBordaToPreference(listPreferenceAvecCycle,nbTests)
    xSansCycle = transferBordaToPreference(listPreferenceSansCycle, nbTests)

    res = transferFromStrToInt(x)
    resSansCycle = transferFromStrToInt(xSansCycle)

    a, b, l, l2, c,restest = testCondition(res)

    a1, b1, l1, l21, c1, restest1 = testCondition(resSansCycle)


    #print(res[0])
    print("le nombre profile non populaire")
    print(len(res))
    print("le nombre profile non populaire a la meme ordre relativement")

    print(a)

    print("Taux de réussite du jugement", (a / len(res)))
    dict = {}
    for key in b:
        dict[key] = dict.get(key, 0) + 1
    print("le nombre d'exception 1")
    print(dict)


    dict={}
    for key in c:
        dict[key] = dict.get(key, 0) + 1
    print("le nombre d'exception 2")
    print(dict)

    #listl = set(l)
    #uniques = np.unique(l,axis=0)
    #print(uniques)
    #print(len(res))
    #print(a)

    #Wlistl2 = set(l2)
    #l3 = listl2 | listl
    print("le nombre profile  populaire")
    print(len(resSansCycle))

    print("le nombre profile  populaire n'a pas  la meme ordre relativement")

    print(len(resSansCycle)-a1)

    print("Taux de réussite du jugement", (len(resSansCycle)-a1)/len(resSansCycle))
    dict = {}
    for key in b1:
        dict[key] = dict.get(key, 0) + 1
    print("le nombre d'exception 1")
    print(dict)

    dict = {}
    for key in c1:
        dict[key] = dict.get(key, 0) + 1
    print("le nombre d'exception 2")
    print(dict)


    #print(resSansCycle)
    #print(res)
main()





