
import sys
import random
import time
import sys


import matplotlib.pyplot as plt
import numpy as np


import numpy

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import memMatching,memMatchingMore5,memMatchingA4, memMatchingA3_A4,randomPathPop, utility, allocTools
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

    #a=Mem
    #b=MemA
    #c=MemA2

    #score borda
    val1=0
    val2=0
    val3=0
    val4=0



    #Rang MaxMin

    val1Rang=0
    val2Rang = 0
    val3Rang = 0
    val4Rang = 0

    while nbDone < nbTests :


        init = allocTools.generateAlloc(nb_resources)
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player,nb_resources)
        print("Preferences = ", preferences)

        #we use these 2 algo to a same instance

        a1,a2 = memMatching.mem_matching(nb_resources, preferences, f, True)
        b1,b2=  memMatchingMore5.mem_matching(nb_resources, preferences, f, True)
        c1,c2 = memMatchingA4.mem_matching(nb_resources,preferences,f,True)
        d1,d2 = memMatchingA3_A4.mem_matching(nb_resources, preferences, f, True)


        big=max([b1,c1,d1])
        if(a1>big):
            val1+=1
        if (a1<b1):
            val2+=1
        if (a1<c1):
            val3+=1
        if (a1<d1):
            val4+=1

        big2 = max([b2, c2, d2])
        if (a2 > big2):
            val1Rang += 1
        if (a2 < b2):
            val2Rang += 1
        if (a2 < c2):
            val3Rang += 1
        if (a2 < d2):
            val4Rang += 1






        nbDone+=1



    return (val1,val2,val3,val4,val1Rang,val2Rang,val3Rang,val4Rang)





def main():
    res = np.zeros([14, 8])
    #list=[[]]*10
    for n in range(4,18):
        random.seed(time.time())
        # global max
        # max = 5
        nbTests = 10000
        listRes = [None] * n
        #global listPreferenceAvecCycle



        # for i in range(4, max)
        val1,val2,val3,val4,val1Rang,val2Rang,val3Rang,val4Rang= testMEMMEMA(nbTests, utility.additive, n)
        #print(a,b,c,d,e,f)

        # print("Score de Borda")
        #
        # print("MEM mieux que MEMA",a)
        # print("MEM mieux que MEMA2",b)
        # print("MEMA mieux que MEMA2", c)
        # print("MEMA mieux que MEM", d)
        # print("MEMA2 mieux que MEM", e)
        # print("MEMA2 mieux que MEMA", f)
        # print("MEMA2 best", x)
        # print("MEMA best", y)
        #
        # print("Rang MaxMin")
        # print("MEM mieux que MEMA", g)
        # print("MEM mieux que MEMA2", h)
        # print("MEMA mieux que MEMA2", i)
        # print("MEMA mieux que MEM", j)
        # print("MEMA2 mieux que MEM", k)
        # print("MEMA2 mieux que MEMA", l)

        # [chr(i) for i in range(97, 123)]
        # cpt=97
        # for j in range(12):
        #     res[i][j]=chr(cpt)
        #     cpt+=1
        # cpt=97


        res[n-4][0]=val1
        res[n-4][1] = val2
        res[n-4][2] = val3
        res[n-4][3] = val4
        res[n-4][4] = val1Rang
        res[n-4][5] = val2Rang
        res[n-4][6] = val3Rang
        res[n-4][7] = val4Rang









    print(res)
    from matplotlib import pyplot
    plt.figure(1)



    barWidth = 0.2

    y1=   [0]*14
    y2 = [0] *14
    y3 = [0] *14
    y4 = [0] *14
    print(y1)
    print(res[0][0])
    #y=[[0]*7 for _ in range(len(res))]
    print(len(res))
    for x in range(0,len(res)):
        #print(x)
        y1[x]=res[x][0]
        y2[x]=res[x][1]
        y3[x]=res[x][2]
        y4[x]=res[x][3]

    #print(y1)
    r1 = range(len(y1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    pyplot.bar(r1, y1, width=barWidth, color=['yellow' for i in y1], label='MEM')

    pyplot.bar(r2, y2, width=barWidth, color=['pink' for i in y2], label='MEMA3>MEM')
    pyplot.bar(r3, y3, width=barWidth, color=['red' for i in y3], label='MEMA4>MEM')
    pyplot.bar(r4, y4, width=barWidth, color=['blue' for i in y4], label='MEMA3+A4>MEM')
    pyplot.xticks([r + barWidth / 2 for r in range(len(y1))],
                  ['n=4', 'n=5', 'n=6', 'n=7', 'n=8', 'n=9', 'n=10', 'n=11', 'n=12','n=13','n=14','n=15','n=16','n=17'])

    pyplot.legend()
    plt.title('Comparasion de Score de Borda')

    #pyplot.show()
    pyplot.figure(2)
    barWidth = 0.2

    y1 = [0] * 14
    y2 = [0] * 14
    y3 = [0] * 14
    y4 = [0] * 14
    print(y1)
    print(res[0][0])
    # y=[[0]*7 for _ in range(len(res))]
    print(len(res))
    for x in range(0, len(res)):
        # print(x)
        y1[x] = res[x][4]
        y2[x] = res[x][5]
        y3[x] = res[x][6]
        y4[x] = res[x][7]

    # print(y1)
    r1 = range(len(y1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    pyplot.bar(r1, y1, width=barWidth, color=['yellow' for i in y1] ,label='MEM')

    pyplot.bar(r2, y2, width=barWidth, color=['pink' for i in y2],label='MEMA3>MEM')
    pyplot.bar(r3, y3, width=barWidth, color=['red' for i in y3],label='MEMA4>MEM')
    pyplot.bar(r4, y4, width=barWidth, color=['blue' for i in y4],label ='MEMA3+A4>MEM')
    pyplot.xticks([r + barWidth / 2 for r in range(len(y1))],
                  ['n=4', 'n=5', 'n=6', 'n=7', 'n=8', 'n=9', 'n=10', 'n=11', 'n=12','n=13','n=14','n=15','n=16','n=17'])

    pyplot.legend()
    plt.title('Comparasion de Rang MaxMin')


    pyplot.show()

main()