
import sys
import random
import time
import sys


import matplotlib.pyplot as plt
import numpy as np


import numpy

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
import memMatching,memMatchingA4, randomPathPop, utility, allocTools,memMatchingA3_A4
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

    aBb=0
    aBc=0
    bBc=0
    bBa=0
    cBa=0
    cBb=0

    aBbRang = 0
    aBcRang = 0
    bBcRang = 0
    bBaRang = 0
    cBaRang = 0
    cBbRang = 0


    x=0
    y=0
    cptMEMABetterBorda=0

    cptMEMBetterRang=0
    cptMEMABetterRang=0
    listspeacilBorda=[]
    listspeacilRang=[]
    cBbBa=0
    bBcBa=0

    while nbDone < nbTests :


        init = allocTools.generateAlloc(nb_resources)
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_borda_diff(nb_player,nb_resources)
        print("Preferences = ", preferences)

        #we use these 2 algo to a same instance

        a1,a2 = memMatching.mem_matching(nb_resources, preferences, f, True)
        b1,b2 = memMatchingA4.mem_matching(nb_resources,preferences,f,True)
        c1,c2 = memMatchingA3_A4.mem_matching(nb_resources, preferences, f, True)


        # print("Score de Borde de MEM est :",ScoreBordaMEM)
        # print("Score de Borde de MEMA est :", ScoreBordaMEMA2)

        if a1 > b1:
            aBb+=1
            #listspeacilBorda.append(preferences)
        if(a1>c1):
            aBc+=1
        if (b1 > c1):
            bBc += 1
        if (b1 > a1):
            bBa += 1
        if (c1 > a1):
            cBa += 1
        if (c1 > b1):
            cBb += 1

        if(c1>b1>=a1):
            cBbBa+=1
        if(b1>c1>=a1):
            bBcBa+=1

        if (a2 > b2):
            aBbRang += 1
            # listspeacilBorda.append(preferences)
        if (a2 > c2):
            aBcRang += 1
        if (b2 > c2):
            bBcRang += 1
        if (b2 > a2):
            bBaRang += 1
        if (c2 > a2):
            cBaRang += 1
        if (c2 > b2):
            cBbRang += 1






        nbDone+=1



    return (aBb,
    aBc,
    bBc,
    bBa,
    cBa,
    cBb,

    aBbRang,
    aBcRang,
    bBcRang,
    bBaRang,
    cBaRang,
    cBbRang,
     cBbBa,bBcBa)





def main():
    res = np.zeros([5, 12])
    #list=[[]]*10
    for n in range(4,9):
        random.seed(time.time())
        global max
        max = 5
        nbTests = 100
        listRes = [None] * n
        #global listPreferenceAvecCycle



        # for i in range(4, max)
        a,b,c,d,e,f,g,h,i,j,k,l,x,y= testMEMMEMA(nbTests, utility.additive, n)
        #print(a,b,c,d,e,f)

        print("Score de Borda")

        print("MEM mieux que MEMA",a)
        print("MEM mieux que MEMA2",b)
        print("MEMA mieux que MEMA2", c)
        print("MEMA mieux que MEM", d)
        print("MEMA2 mieux que MEM", e)
        print("MEMA2 mieux que MEMA", f)
        print("MEMA2 best", x)
        print("MEMA best", y)

        print("Rang MaxMin")
        print("MEM mieux que MEMA", g)
        print("MEM mieux que MEMA2", h)
        print("MEMA mieux que MEMA2", i)
        print("MEMA mieux que MEM", j)
        print("MEMA2 mieux que MEM", k)
        print("MEMA2 mieux que MEMA", l)

        # [chr(i) for i in range(97, 123)]
        # cpt=97
        # for j in range(12):
        #     res[i][j]=chr(cpt)
        #     cpt+=1
        # cpt=97


        res[n-4][0]=a
        res[n-4][1] = b
        res[n-4][2] = c
        res[n-4][3] = d
        res[n-4][4] = e
        res[n-4][5] = f
        res[n-4][6] = g
        res[n-4][7] = h
        res[n-4][8] = i
        res[n-4][9] = j
        res[n-4][10] = k
        res[n-4][11] =l








    print(list)

    # for i in range(len(list)):
    #     print("Score de Borda")
    #
    #     print("MEM mieux que MEMA", list[i][0])
    #     print("MEM mieux que MEMA2", list[i][0])
    #     print("MEMA mieux que MEMA2", list[i][0])
    #     print("MEMA mieux que MEM", list[i][0])
    #     print("MEMA2 mieux que MEM", list[i][0])
    #     print("MEMA2 mieux que MEMA", list[i][0])
    #     print("MEMA2 best", list[i][0])
    #     print("MEMA best", list[i][0])
    #
    #     print("Rang MaxMin")
    #     print("MEM mieux que MEMA", list[i][0])
    #     print("MEM mieux que MEMA2", list[i][0])
    #     print("MEMA mieux que MEMA2", list[i][0])
    #     print("MEMA mieux que MEM", list[i][0])
    #     print("MEMA2 mieux que MEM", list[i][0])
    #     print("MEMA2 mieux que MEMA", list[i][0])

#testMEMMEMA(nbTests, utility.additive, 4)

    #100 Instance
    print(res)
    plt.rcParams['axes.unicode_minus'] = False

    # 指定分组个数
    n_bins = 5

    fig, ax = plt.subplots(figsize=(8, 5))

    # 分别生成10000 ， 5000 ， 2000 个值
    x_multi = [np.random.randn(n) for n in [10, 5, 2]]

    # 实际绘图代码与单类型直方图差异不大，只是增加了一个图例项
    # 在 ax.hist 函数中先指定图例 label 名称
    ax.hist(x_multi, n_bins, histtype='bar',label=list("ABCDE"))

    ax.set_title('多类型直方图')

    # 通过 ax.legend 函数来添加图例
    ax.legend()

    #plt.show()
    #res=np.zeros([5,12])

    x_multi = [np.random.randn(n) for n in [10, 5, 2]]

    print(x_multi[0])
    print(x_multi[1])
    print(x_multi[2])

main()