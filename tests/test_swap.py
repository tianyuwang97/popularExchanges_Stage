
import time
import random

import sys

sys.path.append('/Users/wty123/Desktop/desktop/实习_popular_exchange/popularExchanges-main/Code/housemarkets')

#record the outcomes for a given instance
import allocTools, swap, utility
#from tests import testInstance



import testInstance



def test_swap(nb_try, f, nb_player):
    initTime = time.time()
    nb_resources = nb_player

    allocs = allocTools.all_even_sized_alloc(nb_resources, 1)
    print("Nombre d'allocations differentes : {}".format(len(allocs)))

    res = list()

    r = list(range(nb_resources))
    for i in range(nb_try):
        init = allocs[random.randint(0, len(allocs))]
        print("Allocation initiale : {}".format(init))
        preferences = utility.generate_SP_UP(nb_player, nb_player)
        print("Preferences = ", preferences)
        instance = testInstance.Test_instance(i,init,preferences)

        #test all dynamics
        print('****************C2_0 - Round robin***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=0)
        instance.add_outcome('C2_0', final)
        print("nbswap =" , nbswap)
        print('****************C2_1 - alea uniform ***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=1)
        instance.add_outcome('C2_1', final)
        print("nbswap =", nbswap)
        print('****************C2_2 - alea uniform with priority***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=2)
        instance.add_outcome('C2_2', final)
        print("nbswap =", nbswap)
        print('****************C2_3 - worst off ***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=3)
        instance.add_outcome('C2_3',final )
        print("nbswap =", nbswap)
        print('****************C2_4 - roudn robin on pairs***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=4)
        instance.add_outcome('C2_4', final)
        print('****************C2_5 - alea uniform agents***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=5)
        instance.add_outcome('C2_5', final)
        print('****************C2_6 - alea uniform agents with priority ***************')
        final, nbswap = swap.swap(init, preferences, f, allocs, display=True, test_sequenceable=False, metho_swap=6)
        instance.add_outcome('C2_6', final)
        print("nbswap =", nbswap)
        print('****************C3***************')
        final, nbswap = swap.cycle3(init, preferences, f, allocs, display=True, test_sequenceable=False)
        instance.add_outcome('C3_3',final )
        print("nbswap =", nbswap)
        res.append(instance)

    for e in res:
        print(e)

def main():
    random.seed(time.time())

    test_swap(10, utility.additive, 7)


main()