class statExch (object) :

    def __init__(self, lAg, lRes, nbe) :
        self.lAgents = lAg
        self.lRes = lRes
        self. nbExch = nbe


    def getlAg(self):
        return self.lAgents

    def getlRes(self):
        return self.lRes

    def getNbexch(self):
        return self.nbExch


    def isSame(self, lAg, lRes, size_exch):

        for i in range(size_exch) :

            if self.lAgents[i] != lAg[i] or self.lRes[i] != lRes[i] :
                return -1
        return self.nbExch

    def __str__(self):
        res = "[ {}, {}, nbe= {}".format(self.lAgents,self.lRes, self.nbExch)
        return res


class StateAlloc(object):

    def __init__(self, Alloc):
        self.alloc = Alloc
        self.lStates = []




    def addState(self, state):
        #print("ajout a l alloc {} de l etat {}".format(self.alloc, state))
        self.lStates.append(state)

    def alreadySeenAlloc(self, allocI, n):
        #print("already seen n = {}   alloc Cur = {}  alloc à comparer = {}".format(n,self.alloc, allocI))

        for i in range(n) :
            if allocI[i] != self.alloc[i] :
                return False
        return True


    def alreadyDoneExch(self, lAg, lRes, size_exch):

        for s in self.lStates :
            #print("\t state {}".format(s))
            nbe = s.isSame(lAg, lRes, size_exch )
            if nbe > -1 :
                return  s
        return None

    def equalAlloc(self, alloc, nb_agents):

        for i in range(nb_agents) :
            if self.alloc[i] != alloc.alloc[i] :
                return False
        return True

    def __str__(self):
        res = "alloc = {}, lStates = ".format(self.alloc)
        for e in self.lStates :
            res = res + "\t {}".format(e)
        return res