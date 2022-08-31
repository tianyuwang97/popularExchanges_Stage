
import sys
import random
import time
import sys

import numpy

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import popularMatching, goodHosePathPop, utility, allocTools
import os
#from tests import testInstance

import testInstance


sys.path.insert(0, "..")


def test_goodhouse_path(nbTests, f, nb_player,listPreferenceAvecCycle,max):

    nbDone = 0
    nbPopFound = 0
    nbInstCycle = 0
    propPopular = 0.0
    propNotPopular = 0.0
    nbNotPopFound = 0.0
    nbInstCycleNotProp = 0.0
    listWrong = []

    listRight=[]


    nbPopbutNonPop=0
    nbNonpopbutPop=0
    j = 0
    initTime = time.time()
    nb_resources = nb_player

    #allocs = allocTools.all_even_sized_alloc(nb_resources, 1)
    #print("Nombre d'allocations differentes : {}".format(len(allocs)))

    while nbDone < nbTests :

        # build an instance
        #print("len allocs {}".format(len(allocs)))
        init = allocTools.generateAlloc(nb_resources)
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player,nb_resources)
        print("Preferences = ", preferences)

        # check if there is a popular matching for this instance

        rep = popularMatching.popular_matching(nb_resources, preferences, f, True)


        # if there is a popular matching, run "random path to popular matching"
        # check if a cycle is detected and  that a popular matching is reached

        if rep :
            print("un popular matching existe")
            nbDone = nbDone + 1
            propPopular = propPopular +1
            repRand, nbC,notihng = goodHosePathPop.goodhouse_path_to_popular(init, preferences,f, True)


            if repRand :
                nbPopFound = nbPopFound + 1
                listRight.append(preferences)

            else:
                nbPopbutNonPop=nbPopbutNonPop+1
                #listWrong.append(preferences)


                #raise Exception("WO RI A")
            if nbC >0 :
                nbInstCycle = nbInstCycle +1
        else :
            print("Abraham : no popular")
            nbDone = nbDone + 1
            #listPreferenceAvecCycle[nb_player][j]=str(preferences)
            propNotPopular = propNotPopular + 1
            repRand, nbC ,nothing= goodHosePathPop.goodhouse_path_to_popular(init, preferences, f, True)
            print("nbC = {}".format(nbC))
            j+=1

            #listFuck = []
            if not repRand:
                nbNotPopFound = nbNotPopFound + 1
                nbNonpopbutPop=nbNonpopbutPop+1
                #listWrong.append(preferences)
                #listFuck.append(preferences)

                #raise("Allocation non prop non trouvée comme telle")


            if nbC > 0:
                print("increment")
                nbInstCycleNotProp = nbInstCycleNotProp + 1
                print(nbInstCycleNotProp)
            elif nbC == 0 :
                #raise Exception(" pas populaire et pas de cycles")
                #nbNoCyclebutNoPop=nbInstCycleNotProp + 1

                print("haha")
            print("pas de populaire pouΩ cette instance, skip")
            #raise Exception("pas pop")

    print("nbInstances {} / nbPopFound {} /  nb Pop Instances with cycles {} / nbNOTProp {} / nbNotFound {} / nonPropWithCycles {}/ nbPopbutNonPop {} ".format(nbDone, nbPopFound, nbInstCycle, propNotPopular,nbNotPopFound, nbInstCycleNotProp,nbPopbutNonPop,nbNonpopbutPop))
    print(" /// propPop {} / propNotPop {}".format(propPopular / (propPopular+propNotPopular), propNotPopular/(propPopular+propNotPopular)))
    if(propNotPopular == 0):
        propCycles = 1
    else :
        propCycles = nbInstCycleNotProp / propNotPopular
    return (nbDone, nbPopFound,propPopular ,nbInstCycle, propPopular / (propPopular+propNotPopular),propNotPopular/(propPopular+propNotPopular), nbNotPopFound , propCycles,nbPopbutNonPop,nbNonpopbutPop,listWrong,listRight)



def transfer(preferences):

    sorted_nums = sorted(enumerate(preferences), key=lambda x: x[1], reverse=True)
    idx = [i[0]+1 for i in sorted_nums]
    nums = [i[1] for i in sorted_nums]


    return idx,nums

def main():
    random.seed(time.time())
    global max
    max = 5
    nbTests = 100
    listRes = [None] * max
    global listPreferenceAvecCycle
    listPreferenceAvecCycle =[[" " for i in range (331776)] for j in range(max)]


    #print(listPreferenceAvecCycle)
    for i in range (max-1, max) :
        res = test_goodhouse_path(nbTests, utility.additive, i,listPreferenceAvecCycle,max)
        listRes[i] = res
        if(i%100 == 0) :
            print("{}".format(i))

    #Final Print





    print(" FINAL PRINT")
    for i in range(4, max):
        rep = listRes[i]

        print("nb agents : {} nbInstances {} / nbPopFound {} nombre pop verifer vrai {}where  nb Instances with cycles {} /  propPop {} / propNotPop {} /  nb Non prop not found {} with {} cycles {} {} duck{}{} "
              .format(i, rep[0], rep[1], rep[2], rep[3], rep[4], rep[5], rep[6],rep[7],rep[8],rep[9],rep[10],rep[11]) )


    #print(listPreferenceAvecCycle)

    #for i in range (max):
        #if(listPreferenceAvecCycle[i]!=''):
            #print(listPreferenceAvecCycle[i])

    #os.system("python ".format(listPreferenceAvecCycle))

    #arraycycle=numpy.ndarray(listPreferenceAvecCycle)
    #print(arraycycle)

main()