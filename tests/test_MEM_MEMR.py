
import sys
import random
import time
import sys

import numpy

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import memMatching,memMatchingRandom, randomPathPop, utility, allocTools
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
    while nbDone < nbTests :


        init = allocTools.generateAlloc(nb_resources)
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player,nb_resources)
        print("Preferences = ", preferences)

        #we use these 2 algo to a same instance

        ScoreBordaMEM,RangMaxMinMEM = memMatching.mem_matching(nb_resources, preferences, f, True)
        ScoreBordaMEMA,RangMaxMinMEMA =memMatchingRandom.mem_matching(nb_resources,preferences,f,True)


        print("Score de Borde de MEM est :",ScoreBordaMEM)
        print("Score de Borde de MEMA est :", ScoreBordaMEMA)

        if(ScoreBordaMEM>ScoreBordaMEMA):
            cptMEMBetterBorda+=1
            listspeacilBorda.append(preferences)

        elif(ScoreBordaMEM<ScoreBordaMEMA):
            cptMEMABetterBorda+=1

        if(RangMaxMinMEM>RangMaxMinMEMA):
            cptMEMBetterRang+=1
            listspeacilRang.append(preferences)
        elif(RangMaxMinMEM<RangMaxMinMEMA):
            cptMEMABetterRang+=1

        nbDone+=1



    return cptMEMBetterBorda,cptMEMABetterBorda,cptMEMBetterRang,cptMEMABetterRang,listspeacilBorda,listspeacilRang





def main():
    random.seed(time.time())
    global max
    max = 4
    nbTests = 10000
    listRes = [None] * max
    #global listPreferenceAvecCycle



    # for i in range(4, max)
    a,b,c,d,e,f = testMEMMEMA(nbTests, utility.additive, 4)
    print(a,b,c,d,e,f)
    #testMEMMEMA(nbTests, utility.additive, 4)

    #100 Instance




main()