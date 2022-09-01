
import sys
import numpy as np

sys.path.insert(0, "..")

from housemarkets import utility


def compare(pref1, pref2, nbR):
    cpt = 0
    cptTot = 0
    #print(pref1, pref2)
    for i in range(1,nbR+1):
        k=0
        indI1 = -1
        indI2 = -1
        while k < nbR and pref1[k] != i:
            k = k +1
        indI1 = k
        k = 0
        while k < nbR and pref2[k] != i:
            k = k + 1
        indI2 = k
        for j in range(i+1, nbR+1):

            k = 0
            indJ1 = -1
            indJ2 = -1
            while k < nbR and pref1[k] != j:
                k = k + 1
            indJ1 = k
            k = 0
            while k < nbR and pref2[k] != j:
                k = k + 1
            indJ2 = k

            if(indI1 > indJ1 and indI2 < indJ2) or (indJ1 > indI1 and indJ2 < indI2) :
                cpt = cpt +1
            cptTot = cptTot +1
    return cpt, cptTot



def tirage_pref_SP(nbR,nbTirages, typeSP):

    if(typeSP == 0):
       return utility.generate_SP_UP(nbTirages, nbR)
    else:
        return utility.generate_SP_IP(nbTirages, nbR)



def test_for_rFixed(nbR, nbTirages, typeSP):
    cpt = 0
    cptTot = 0
    for i in range(nbTirages) :
        if(typeSP == 0) :
            pref1 = utility.single_peaked_UP(nbR)
            pref2 = utility.single_peaked_UP(nbR)
        else :
            pref1 = utility.single_peaked_IP(nbR)
            pref2 = utility.single_peaked_IP(nbR)

        n1, n2 = compare(pref1, pref2, nbR)
        cpt += n1
        cptTot += n2

    return cpt, cptTot


def test_probaPref(minR, maxR, nbTirages, typeSP):
    res = dict()

    for i in range(minR, maxR+1):
        print("nb ressources = {}".format(i))
        cpt, cptTot = test_for_rFixed(i, nbTirages, typeSP )
        print(cpt, cptTot)
        if cptTot> 0 :
            res[i] = cpt/cptTot
        else:
            res[i] = 0
    return res


def average_rank(pref, nbR, nbTirages):
    res = numpy.zeros(nbR)
    for i in range(nbR):
        somme = 0
        for j in range(nbR):
           somme = somme + pref[i][j]*(j+1)
        somme = somme /nbTirages
        res[i] = somme
    return res

def test_rank(minR,maxR, nbTirages):

    for i in range(minR, maxR+1) :
        for typeSP in range(2):
            res = numpy.zeros((i,i))
            for k in range(nbTirages):
                if (typeSP == 0):
                    pref1 = utility.single_peaked_UP(i)
                else:
                    pref1 = utility.single_peaked_IP(i)
                for j in range(i):
                    #print(pref1)
                    res[j][round(pref1[j])-1] = res[j][round(pref1[j])-1] +1
            #print_res(res,typeSP,i)
            print("ressorces {}, type {} : \n{}".format(i,typeSP,res))
            print(average_rank(res,i,nbTirages))


def print_res(res, type,  nbR):
    sres =''+str(nbR)+ " ressources "
    if(type ==0):
        sres = sres +"SPUP : "
    else:
        sres = sres +"SPIP"
    for i in range(nbR) :
        sres = sres+ " r"+ str(i)+ " : ["
        for k in range(nbR):
            sres = sres +str(res[i][k])+ ' , '
            sres = sres + "] \n"
    print(sres)


###############################################################################
# Computes a few diversity indices
# see 
###############################################################################


def rank(pref,res):
    """
    returns the rank of res in pref
    """
    return int(pref[res])


def compute_kd_dist(pref1,pref2,nbR):
    """
    compute kendal-tau distance between two rankings pref1 and pref2
    """
    assert len(pref1)==len(pref2)
    pairwise_match = [(x,y) for x in range(0,nbR) for y in range(0,nbR) if np.sign(rank(pref1,x) - rank(pref1,y)) == np.sign(rank(pref2,y)-rank(pref2,x)) and x!=y]    
    #print(pairwise_match)
    return 0.5*len(pairwise_match)

def compute_spearman_dist(pref1,pref2,nbR):
    """
    computes spearman distance between two rankings pref1 and pref2
    """
    spearman=0
    ranks_of_resources = [(rank(pref1,r),rank(pref2,r)) for r in range(0,nbR)]
    #print(ranks_of_resources)
    for (x,y) in ranks_of_resources:
        spearman+=abs(x-y)
    return spearman

def compute_dist_profile(profile,dist):
    """
    computes the distance for a profile, for a dist (kendal/spearman)
    """
    size = len(profile)
    nbR = len(profile[0])
    diversity=0
    for i in range(size): 
        for j in range(i+1,size): 
            if dist=="kendall":
                diversity+=compute_kd_dist(profile[i],profile[j],nbR)
            if dist=="spearman":
                diversity+=compute_spearman_dist(profile[i],profile[j],nbR)  
    return diversity

def normalized_diversity(profile,dist): 
    return


def averaged_diversity(nbA,nbR,SP,dist,nb_exps):
    div=0
    max_dist=0
    for i in range(nb_exps):
        profile=tirage_pref_SP(nbR,nbA,SP)
        d=compute_dist_profile(profile,dist)
        div+=d
        if d>max_dist:
            max_dist=d
    return div/nb_exps, max_dist

def averaged_all_diversity(nbA,nbR,SP,nb_exps):
    dk=0
    ds = 0 # diversity in SP/Kendal, SP/Spearman 
    div_k = 0 
    div_s=0
    max_dk = 0 
    max_ds = 0
    for i in range(nb_exps):
        profile=tirage_pref_SP(nbR,nbA,SP)
        dk=compute_dist_profile(profile,"kendall")
        ds=compute_dist_profile(profile,"spearman")
        div_k+=dk
        div_s+=ds
        if dk>max_dk:
            max_dk=dk
        if ds>max_ds:
            max_ds=ds
    return div_k/nb_exps, max_dk, div_s/nb_exps, max_ds


        


def main():
    #print(test_probaPref(2,5, 100000, 0))
    #test_rank(2, 10, 100000)
    
    ## testing divesity measures
    #profile = tirage_pref_SP(5, 3, 0)
    #print(profile[0]. astype(int))
    #print(profile)
    ## testing kendall-tau
    #print(compute_kd_dist(profile[0], profile[1], 5))
    #print(compute_dist_profile(profile,"kendall"))
    ## testing spearman
    #print(compute_spearman_dist(profile[0], profile[1], 5))
    #print(compute_dist_profile(profile,"spearman"))
    ## average diversity on a number of trials
    #print(freq_rank(7, 2, 0))

    print("UP-SP: ", averaged_all_diversity(7, 7, 0, 10000))
    print("IC-SP: ", averaged_all_diversity(7, 7, 1, 10000))
    
    
    
    #print("Average Kendall under UP-SP ", averaged_diversity(7,7,0,"kendall",10000))
    #print("Average Kendall under IC-SP ", averaged_diversity(7,7,1,"kendall",10000))
    #print("Average Spearman under UP-SP ", averaged_diversity(7,7,0,"spearman",10000))
    #print("Average Spearman under IC-SP ", averaged_diversity(7,7,1,"spearman",10000))

main()