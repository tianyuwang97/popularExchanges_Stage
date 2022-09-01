
#from housemarkets import allocTools

import allocTools

# Classe pour un agent, num c'est son id, SP ses préférences (qui ne sont pas nécessairement SP...),
# u son type d'utilité (additive, max, min) et initial son bundle de base
class Player(object):

    def __init__(self, num, initial, SP, u):
        self.num = num
        self.SP = SP
        self.u = u
        self.bundle = initial

    # Calcule l'utilité du bundle passé en paramètre
    def utility(self, b):
        return self.u(b, self.SP)

    # Calcule l'utilité courante de l'agent
    def selfutility(self):
        return self.u(self.bundle, self.SP)

    # Applique le swap pour les biens b1 et b2 à l'agent
    def swap(self, b1, b2):

        for b in b1:
            self.bundle.remove(b)
        self.bundle += list(b2)


    def get_best_item(self, size):

        return allocTools.max_tab(self.SP, size)

    def get_best_item_restr(self, lFreeHouses, nbFreeHouses):
        bestItem = lFreeHouses[0]
        for i in lFreeHouses[1:] :
            if self.SP[i] > self.SP[bestItem] :
                bestItem = i

        return bestItem

    def get_good_item(self,size,tab2,listPre):
        return allocTools.max_good_tab(self.SP,size,tab2,listPre)
    def get_bad_item(self,size,tab2,listPre):
        return allocTools.max_bad_tab(self.SP,size,tab2,listPre)
    def get_good_item2(self,size,tab2,tab3,listPre):
        return allocTools.max_good_tab2(self.SP,size,tab2,tab3,listPre)



    def get_best_sec_item(self,size, tab):

        return allocTools.max_sec_tab(self.SP, size, tab)


    def get_best_sec_item_restr(self, isFH, lFreeHouses, nbFreeHouses):
        e = 0
        while (e < nbFreeHouses and isFH[lFreeHouses[e]] == True):
            e = e + 1
        if e == nbFreeHouses:
            return -1
        else:
            maxC = e
            for e2 in range(e + 1, nbFreeHouses):
                if self.SP[lFreeHouses[e2]] > self.SP[maxC] and isFH[lFreeHouses[e2]] == False:
                    maxC = e2
            return lFreeHouses[maxC]


    def assign_bundle(self, b):
        self.bundle = b

    def __eq__(self, other):
        if (isinstance(self, other.__class__)):
            return self.num == other.num
        return False

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Player" + str(self.num) + "\n\tUtility: " + str(self.SP) + "\n\tBundle: " + str(self.bundle) + "\n"

    def __repr__(self):
        return self.__str__()
