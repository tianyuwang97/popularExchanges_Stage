import numpy as np
import copy
import utility
import sys
import itertools
import time


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
        self.bundle += b2










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


# Génère tous les subsets de l
def subsets(l):
    l = copy.deepcopy(l)
    res = [l]
    s = set(l)
    for i in range(len(l)):
        for sub in set(itertools.combinations(s, i)):
            if len(sub) != 0:
                res.append(list(sub))
    return res


# Génère les subsetsde l d'une taille donnée
def subset(l, size):
    if size == 1:
        return [[i] for i in l]
    else:
        return [list(i) for i in itertools.combinations(l, size)]


# Retourne tous les découpages possible d'une liste en n éléments de taille non nulle
def slices(l, n):
    global resf
    resf = []




    def aux(l, n, restmp):
        if n == len(l):
            return restmp + [[i] for i in l]
        elif n == 1:
            return restmp + [l]
        else:
            for k in range(len(l) + 1 - n):
                resf.append(aux(l[k + 1:], n - 1, restmp + [l[:k + 1]]))

    if n == len(l):
        return [[[i] for i in l]]
    else:
        aux(l, n, [])
        return [i for i in resf if i != None]


# Retourne toutes les permutations de [[1, size]]
def index_permutation(size):
    def aux(size, result, level=0, item=None):
        if level >= size:
            result.append(item[:])
            return
        if item == None:
            item = [-1 for i in range(size)]
        for index in range(size):
            if item[index] < 0:
                item[index] = level
                aux(size, result, level + 1, item)
                item[index] = -1
        return result

    return aux(size, [])


# Génère toutes les alloc possibles
def all_alloc(nb_resources, nb_player):
    res = []
    for l in index_permutation(nb_resources):
        res += slices(l, nb_player)
    return res


# Génère toutes les alloc où les agents ont le même nombre de ressources
def all_even_sized_alloc(nb_resources, nb_resource_per_player):
    res = []
    for r in index_permutation(nb_resources):
        res.append([r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)])
    return res


# Truc le plus moche du monde, test Pareto en testant toutes les alloc possibles
def isPareto(players, nb_resources, allocs):
    def isBetterAll(a, players):
        onebetter = False
        for p in players:
            if p.utility(a[p.num]) < p.selfutility():
                return False
            elif p.utility(a[p.num]) > p.selfutility():
                onebetter = True
        #		if onebetter:
        #				print("\n\t\t!!!!!!!!!!!!!!!!!!\np = " + str(players) + " a = " + str(a) + "\n")
        #				sys.exit(0)
        return onebetter

    if allocs is None:
        allocs = all_alloc(nb_resources, len(players))
    for a in allocs:
        if isBetterAll(a, players):
            return False
    return True


# Run les échanges swap
def swap(initial, utilities, u, allocs=None, test_Pareto=False, test_frustrating=False,
         test_sequenceable=False, display=False):
    # Test tous les swaps possibles et applique le premier réalisable, return False si un swap réalisé, True sinon
    def swap_aux(players):
        for swap_length in [1, 2]:
            for p1 in players:
                for p2 in players[p1.num + 1:]:
                    #					print("P1 {}".format(subset(p1.bundle, swap_length)))
                    #					print("P2 {}".format(subset(p2.bundle, swap_length)))
                    for b1 in subset(p1.bundle, swap_length):
                        for b2 in subset(p2.bundle, swap_length):
                            newb1 = p1.bundle + b2
                            for tmp in b1:
                                newb1.remove(tmp)
                            newb2 = p2.bundle + b1
                            #							print("Je test b1 = {}, b2 = {}\nnewb1 = {}, newb2 = {}".format(b1, b2, newb1, newb2))
                            for tmp in b2:
                                newb2.remove(tmp)
                            if ((p1.utility(newb1) >= p1.selfutility()
                                 and p2.utility(newb2) > p2.selfutility())
                                    or (p1.utility(newb1) > p1.selfutility()
                                        and p2.utility(newb2) >= p2.selfutility())):
                                if display:
                                    print("{} donne {} à {} qui lui donne {}".format(p1.num, b1, p2.num, b2))
                                p1.swap(b1, b2)
                                p2.swap(b2, b1)
                                return False
        #							print("J'ai pas échangé")
        return True

    # Initialisation des agents
    initial = copy.deepcopy(initial)
    players = [Player(i, initial[i], utilities[i], u) for i in range(len(initial))]
    nb_resources = sum([len(i) for i in initial])

    if display:
        print("\nINIT")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        print("\nSWAP")

    # Tant qu'il y a des swaps possible, on les applique
    finished = False
    while not finished:
        finished = swap_aux(players)

    if display:
        print("\nEND")
        for p in players:
            print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))

    # Si demandé on test si l'alloc est Pareto opti
    if test_Pareto:
        PO = isPareto(players, nb_resources, allocs)
        if not PO:
            if display:
                tmp = []
                for p in players:
                    tmp.append(p.bundle)
                print("Pas Pareto optimal:\nUtilities : {}\nInit : {}\nEnd : {}".format(utilities, initial, tmp))
                for p in players:
                    print("{}: u({}) = {}".format(p.num, p.bundle, p.selfutility()))
        return PO

    # Si demandé on test si l'alloc est frustrante
    if test_frustrating:
        tmp = False
        for p in players:
            if np.argmax(p.SP) in p.bundle:
                tmp = True
        if not tmp:
            print("==============================")
            for i in players:
                print("Agent {}: top={} {} {}".format(i.num, np.argmax(i.SP), i.bundle, i.SP))
        return tmp

    # Si demandé on test si l'alloc est sequenceable
    if test_sequenceable:
        if not utility.is_sequenceable(players):
            print(players)
            isPareto(players, nb_resources, None)
        return utility.is_sequenceable(players)

    if display:
        print("Sequenceable : {}".format(utility.is_sequenceable(players)))
    return True


# Affiche un run des échanges swap
def print_swap(nb_player, nb_resource_per_player, u, pref):
    nb_resources = nb_player * nb_resource_per_player
    init = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    p = pref(nb_player, nb_resources)
    print("PREFERENCES")
    for a in range(len(p)):
        print("{} : {}".format(a, p[a]))
    return swap(init, p, u, display=True)


# Compte le nombre d'alloc PO sur nb_try
def count_nb_Pareto(nb_try, f, nb_player, nb_resource_per_player, preferences, even_size=True):
    initTime = time.time()
    nb_resources = nb_player * nb_resource_per_player
    print("Nombre d'Optimum de Pareto pour {} joueurs et {} ressources avec la fonction {}, {} essais".format(
        nb_player, nb_resources, f.__name__, nb_try))

    if even_size:
        allocs = all_even_sized_alloc(nb_resources, nb_resource_per_player)
    else:
        allocs = all_alloc(nb_resources, nb_player)
    print("Nombre d'allocations différentes : {}".format(len(allocs)))

    res = 0
    init = []
    tmp = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    print("Allocation initiale : {}".format(init))

    for i in range(nb_try):
        if i % (nb_try / 10) == 0:
            print("Essai {} : nombre de non Pareto {} sur {}".format(i, res, i))
        if not swap(init, preferences(nb_player, nb_resources), f, allocs, test_Pareto=True):
            res += 1
    print("Nombre d'état stationnaire de swap non Pareto optimal : {} sur {}".format(res, nb_try))
    print("Temps de calcul du nombre de Pareto : {} secondes".format(time.time() - initTime))
    return res


# Compte le nombre d'alloc sequenceable sur nb_try
def count_nb_Seq(nb_try, f, nb_player, nb_resource_per_player, preferences, even_size=True):
    initTime = time.time()
    nb_resources = nb_player * nb_resource_per_player
    print("Nombre d'equilibre séquenceable pour {} joueurs et {} ressources avec la fonction {}, {} essais".format(
        nb_player, nb_resources, f.__name__, nb_try))

    if even_size:
        allocs = all_even_sized_alloc(nb_resources, nb_resource_per_player)
    else:
        allocs = all_alloc(nb_resources, nb_player)
    print("Nombre d'allocations différentes : {}".format(len(allocs)))

    res = 0
    init = []
    tmp = []
    r = list(range(nb_resources))
    init = [r[i:i + nb_resource_per_player] for i in range(0, nb_resources, nb_resource_per_player)]
    print("Allocation initiale : {}".format(init))

    for i in range(nb_try):
        if i % (nb_try / 10) == 0:
            print("Essai {} : nombre de non séquenceable {} sur {}".format(i, res, i))
        if not swap(init, preferences(nb_player, nb_resources), f, allocs, test_sequenceable=True):
            res += 1
    print("Nombre d'état stationnaire de swap non séquenceable optimal : {} sur {}".format(res, nb_try))
    print("Temps de calcul du nombre de séquenceable : {} secondes".format(time.time() - initTime))
    return res


def main():
    #	print(index_permutation(15))
    count_nb_Seq(100, utility.additive, 3, 2, utility.generate_mixt)


#	swap([[1, 0], [2, 3]], [np.array([22, 18, 17, 16]), np.array([15, 4, 4, 3])], utility.additive)
#	print(utility.attachement_digraph([np.array([4, 5, 10, 8]), np.array([8, 8, 10, 6]), np.array([5, 5, 8, 6])]))
#	print(utility.to_order([[3, 4, 2, 1], [2, 3, 4, 1], [1, 2, 3, 4], [4, 1, 2, 3]]))
#	print_swap(3, 2, utility.additive, utility.generate_SP_indif)

main()