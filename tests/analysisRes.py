

import sys
sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')

import utility
#from housemarkets import utility

#record the outcomes of the different dynamics for a MARA instance
class analysisRes(object):


    def __init__(self, nbRuns, minNbAg, maxNbAg, step, metho):
        self.perfSWE = dict()
        self.perfSWU = dict()
        self.nbSwap = dict()
        self.diffAllocSWE = dict()
        self.diffAllocSWU = dict()
        self.minDiffSWU = dict()
        self.maxDiffSWU = dict()
        self.minDiffSWE = dict()
        self.maxDiffSWE = dict()
        self.methodos = metho # ["C2_0", "C2_1", "C2_2", "C2_3", "C2_4", "C3_3", "crawler", "maxUtiIR", "maxEgalIR"]
        self.nbRuns = nbRuns
        self.minNbAg = minNbAg
        self.maxNbAg = maxNbAg
        self.step = step



    def anlyseExperiments(self,  dictRes):

        print("******************* EXPERIMENTS ANALYSIS *********************")

        for i in range(self.minNbAg, self.maxNbAg + 1, self.step):
            print ("nbagents",i)
            resUtil = dict()
            resEgal = dict()
            resMinDiffSWU = dict()
            resMaxDiffSWU = dict()
            resMinDiffSWE = dict()
            resMaxDiffSWE = dict()
            resnbSwap = dict()

            for j in range (0, self.nbRuns):
                #print("\t nb runs ", j)
                idInst = str(i) + "_" + str(j)
                dictOneInstance = dictRes[idInst]
                #print("instance", dictOneInstance)
                prefAg = dictOneInstance["pref"]
                #print(" \t pref =" , prefAg)
                #get optimal SWU of the instance
                optiAllocSWU = dictOneInstance["maxUti"]
                optiSwU, temp = utility.evalAlloc(optiAllocSWU,prefAg,i)
                #print("\t\t optialloc SWU ", optiAllocSWU)
                #get optimal SWE of the instance
                optiAllocSWE = dictOneInstance["maxEgal"]
                temp, optiSwE = utility.evalAlloc(optiAllocSWE,prefAg,i)
                #print("\t\t optialloc SWE ", optiAllocSWE)
                #print("\t\t opti SWU = ", optiSwU, "opti SWE = ", optiSwE)

                for m in self.methodos:
                    #for each allocation methods evaluated
                    #print("\t\t methodo :", m)
                    alloc = dictOneInstance[m]
                    #print("\t\t alloc ", alloc)
                    swU, swE = utility.evalAlloc(alloc, prefAg, i)
                    #print("\t\t \t alloc SwU = ", swU, "alloc SwE = ", swE)
                    percSwU = swU / optiSwU
                    percSwE = swE / optiSwE
                    #print("\t\t \t perc SwU = ", percSwU, "perc SwE = ", percSwE)
                    if(j == 0) :
                        resUtil[m] = percSwU
                        resEgal[m] = percSwE
                        resMinDiffSWU[m] = percSwU
                        resMaxDiffSWU[m] = percSwU
                        resMinDiffSWE[m] = percSwE
                        resMaxDiffSWE[m] = percSwE
                    else :
                        tempU =resUtil[m]
                        tempE = resEgal[m]
                        resUtil[m] = percSwU + tempU
                        resEgal[m] = percSwE + tempE
                        if(percSwU < resMinDiffSWU[m] ) :
                            resMinDiffSWU[m] = percSwU
                        if(percSwU > resMaxDiffSWU[m]) :
                            resMaxDiffSWU[m] = percSwU
                        if (percSwE < resMinDiffSWE[m]):
                            resMinDiffSWE[m] = percSwE
                        if (percSwE > resMaxDiffSWE[m]):
                            resMaxDiffSWE[m] = percSwE


                    if (m.startswith("C2") or m.startswith("C3") or m.startswith("ttc") or m.startswith("crawler")) : #number of swaps to register
                        key = m + "_NBSw"
                        nbswap = dictOneInstance[key]
                        print("*******************" + m )
                        if(j == 0):
                            resnbSwap[m] = nbswap
                            print("nbswap =" + str(nbswap))
                        else:
                            resnbSwap[m] = nbswap + resnbSwap[m]
                            print("nbswap ="+ str(resnbSwap[m]))


            #all instances of a given size have been considered
            for e in resUtil.keys():
                resUtil[e] = resUtil[e] / self.nbRuns
            for e in resEgal.keys():
                resEgal[e] = resEgal[e] / self.nbRuns

            self.perfSWU[i] = resUtil
            self.perfSWE[i] = resEgal
            self.nbSwap[i] = resnbSwap
            self.maxDiffSWE[i] = resMaxDiffSWE
            self.minDiffSWE[i] = resMinDiffSWE
            self.maxDiffSWU[i] = resMaxDiffSWU
            self.minDiffSWU[i] = resMinDiffSWU






    def printAnalysis(self):
        output = "OUTPUT of the analysis \n"

        output = output + " ******* SWU **** \n"

        line = "nb ag \t"
        for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
            line = line + str(i)+ "\t"
        output = output + line + "\n"

        for m in self.methodos :
            line = m + "\t"

            for i in range(self.minNbAg, self.maxNbAg +1,self.step) :
                temp = self.perfSWU[i]
                line = line + str(temp[m]) + "\t"

            output = output + line
            line = "\n maxdiff \t"

            for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                temp = self.maxDiffSWU[i]
                line = line + str(temp[m]) + "\t"

            output = output + line
            line = "\n mindiff \t"

            for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                temp = self.minDiffSWU[i]
                line = line + str(temp[m]) + "\t"

            output = output + line + "\n"

        output = output + " ******* SWE **** \n"

        line = "nb ag \t"
        for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
            line = line + str(i) + "\t"
        output = output + line + "\n"

        for m in self.methodos:
            line = m + "\t"

            for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                temp = self.perfSWE[i]
                line = line + str(temp[m]) + "\t"

            output = output + line
            line = "\n maxdiff \t"

            for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                temp = self.maxDiffSWE[i]
                line = line + str(temp[m]) + "\t"

            output = output + line
            line = "\n mindiff \t"

            for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                temp = self.minDiffSWE[i]
                line = line + str(temp[m]) + "\t"

            output = output + line + "\n"


        output = output + " ******* nbSwaps **** \n"

        for m in self.methodos:
            if (m.startswith("C2") or m.startswith("C3") or m.startswith("ttc") or m.startswith("crawler")):
                line = m + "\t"
                if(m.startswith("ttc")):
                    line = line + "\t"
                for i in range(self.minNbAg, self.maxNbAg + 1,self.step):
                    temp = self.nbSwap[i]
                    line = line + str(temp[m]) + "\t"

                output = output + line + "\n"

        return output

if __name__ == "__main__":
   def main():

      utility.test()
      #print("hello")


   main()