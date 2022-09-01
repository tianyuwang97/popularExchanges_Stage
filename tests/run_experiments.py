import time
import random
import json
import datetime
import numpy as np


import sys
sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')
#record the outcomes for a given instance
import allocTools, swap, utility, crawler, rank_optimal, ttc
#from tests import testInstance, analysisRes
import testInstance, analysisRes

def run_expe_Nplayers(nb_try, f, nb_player,geneSP, res,):

    # run experiments for a given size of instances

    nb_resources = nb_player

   # allocs = allocTools.all_even_sized_alloc(nb_resources, 1)
   # print("Nombre d'allocations differentes : {}".format(len(allocs)))



    r = list(range(nb_resources))
    for i in range(nb_try):
        #indice = random.randint(0, len(allocs)-1)
        #init = allocs[indice]

        print("***************** EXPE  nbag =",nb_player, " run ", i )

        arr = np.arange(nb_resources)
        np.random.shuffle(arr)
        init = [[int(e)] for e in arr] #int required for the list to be serializable with Json
       # print("Allocation initiale : {}".format(init))

        if(geneSP == -1): # generate impartial culture (no SP)
            preferences = utility.generate_rand_unif(nb_player, nb_player,nb_player)
        elif(geneSP == 1) :
            preferences = utility.generate_SP_UP(nb_player, nb_player)
        else :
            preferences = utility.generate_SP_IP(nb_player,nb_player)
        #print("Preferences = ", preferences)
       # instance = testInstance.Test_instance(i,init,preferences)
        instance = dict()
        instance["num"]=i
        instance["init"] = init
        instance["pref"] = preferences
        #test all dynamics
        print("C2_0")
        final , nbswap = swap.swap(init, preferences, f,  display=False, test_sequenceable=False, metho_swap=0)
        instance['C2_0'] = final
        instance['C2_0_NBSw'] = nbswap

        print("C2_1")
        final, nbswap = swap.swap(init, preferences, f,  display=False, test_sequenceable=False, metho_swap=1)
        instance['C2_1'] = final
        instance['C2_1_NBSw'] = nbswap

        print("C2_2")
        final, nbswap = swap.swap(init, preferences, f, display=False, test_sequenceable=False, metho_swap=2)
        instance['C2_2'] = final
        instance['C2_2_NBSw'] = nbswap

        print("C2_3")
        final, nbswap = swap.swap(init, preferences, f,  display=False, test_sequenceable=False, metho_swap=3)
        instance['C2_3'] = final
        instance['C2_3_NBSw'] = nbswap

        print("C2_4")
        final, nbswap = swap.swap(init, preferences, f,  display=False, test_sequenceable=False, metho_swap=4)
        instance['C2_4'] = final
        instance['C2_4_NBSw'] = nbswap

        print("C2_5")
        final, nbswap = swap.swap(init, preferences, f, display=False, test_sequenceable=False, metho_swap=5)
        instance['C2_5'] = final
        instance['C2_5_NBSw'] = nbswap

        print("C2_6")
        final, nbswap = swap.swap(init, preferences, f, display=False, test_sequenceable=False, metho_swap=6)
        instance['C2_6'] = final
        instance['C2_6_NBSw'] = nbswap

        print("C3_3")
        final, nbswap = swap.cycle3(init, preferences, f,  display=False, test_sequenceable=False)
        instance['C3_3'] = final
        instance['C3_3_NBSw'] = nbswap

        print("Crawler")
        axis = [i for i in range(nb_player)]
        final, nbCC, sizeC, minC, maxC, nbSwaps = crawler.crawlerLR(preferences,nb_player, crawler.changeFormatAllocInput(init), axis,True)
        instance['crawler'] = crawler.changeFormatAllocOutput(final)
        instance['crawler_NBCyc'] = nbCC
        instance['crawler_Size'] = sizeC
        instance['crawler_max_Size'] = maxC
        instance['crawler_min_Size'] = minC
        instance['crawler_NBSw'] = nbSwaps

        print("maxUti_IR")
        final = rank_optimal.maxUtilitarianIR(init,preferences)
        instance['maxUtiIR'] = final

        print("maxEgal_IR")
        final = rank_optimal.maxEgalitarianIR(init, preferences)
        instance['maxEgalIR'] = final

        print("maxUti")
        final = rank_optimal.maxUtilitarian(init, preferences)
        instance['maxUti'] = final

        print("maxEgal")
        final = rank_optimal.maxEgalitarian(init, preferences)
        instance['maxEgal'] = final

        print("TTC")
        final, size, nbC, minC, maxC,nbSwaps = ttc.our_format_ttc(nb_player, preferences,init)
        instance['ttc'] = final
        instance['TTC_NBCyc'] = nbC
        instance['TTC_Size'] = size
        instance['TTC_min_Size'] = minC
        instance['TTC_max_Size'] = maxC
        instance['ttc_NBSw'] = nbSwaps

        key = str(nb_player)+ "_"+str(i)
        res[key] = instance


   # for e in res:
    #    print(e)



class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
             return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def run_expe_range_players(nbtry, f, minP, maxP, geneSP, step= 1):

    dictRes = dict()

    string_geneSP = ""
    if (geneSP == -1):
        string_geneSP = "IC"
    elif (geneSP == 1):
        string_geneSP = "SPUP"
    else:
        string_geneSP = "SPIP"


    for i in range(minP, maxP+1,step):
        print("run expe for size: "+str(i))
        run_expe_Nplayers(nbtry,f,i,geneSP, dictRes)
    json_string = json.dumps(dictRes,cls=NumpyEncoder)
    now = datetime.date.today()
    fileName = "output_"+string_geneSP+ "_"+str(minP)+"_"+str(maxP)+"_"+str(nbtry)+"_"+str(now)
    print(fileName)
    file = open(fileName,"w")
    file.write(json_string)
    file.close()
    #analysis = analysisRes.analysisRes(nbtry,minP,maxP,step,["C2_0", "C2_1", "C2_2", "C2_3", "C2_4", "C3_3", "crawler", "maxUtiIR", "maxEgalIR","ttc"])
    analysis = analysisRes.analysisRes(nbtry, minP, maxP, step,
                                       ["C2_0", "C2_1", "C2_2", "C2_3", "C2_4", "C2_5", "C2_6", "C3_3",  "maxUtiIR",
                                        "maxEgalIR", "ttc","crawler"])

    analysis.anlyseExperiments(dictRes)



    fileName = "summary_" +string_geneSP+ "_"+ str(minP) + "_" + str(maxP) + "_" + str(nbtry) + "_" + str(now)
    print(fileName)
    s =  analysis.printAnalysis()
    file = open(fileName, "w")
    file.write(s)
    print(s)
    file.close()





def main():
    random.seed(0)
    initTime = time.time()
    run_expe_range_players(1000, utility.additive, 35,40, 1,5)
    endTime = time.time()
    print("processing time", endTime - initTime)

main()
