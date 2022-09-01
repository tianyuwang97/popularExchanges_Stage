
import sys
import random
import time
import sys

import numpy

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import  randomPathPop, utility, allocTools,MaxSB
import os
#from tests import testInstance

import testInstance
sys.path.insert(0, "..")


def testMEMMEMA(nbTests, f, nb_player):

    nbDone = 0
    nbPopFound = 0
    nbInstCycle = 0
    propPopular = 0.0
    propNotPopular = 0.0
    nbNotPopFound = 0.0
    nbInstCycleNotProp = 0.0
    j = 0
    initTime = time.time()
    nb_resources = nb_player
    cptMEMBetterBorda=0
    cptMEMABetterBorda=0

    cptMEMBetterRang=0
    cptMEMABetterRang=0
    listspeacilBorda=[]
    listspeacilRang=[]
    cpt=0
    while nbDone < nbTests :


        init = allocTools.generateAlloc(nb_resources)
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player,nb_resources)
        print("Preferences = ", preferences)



        ScoreBordaMEM,OK= MaxSB.test(nb_resources, preferences, f, True)
        print("Score de Borde de MEM est :",ScoreBordaMEM)
        #listspeacilBorda.append((ScoreBordaMEM))

        if OK:
            cpt+=1
        else:
            listspeacilBorda.append(preferences)



        nbDone+=1

    print(nbDone)


    return cptMEMBetterBorda,listspeacilBorda,cpt





def main():
    random.seed(time.time())
    global max
    max = 4
    nbTests = 1000
    listRes = [None] * max
    #global listPreferenceAvecCycle



    # for i in range(4, max)
    a,b,c = testMEMMEMA(nbTests, utility.additive, 4)

    print(b)
    print(len(b))
    print(c)


    #testMEMMEMA(nbTests, utility.additive, 4)

    #100 Instance




main()