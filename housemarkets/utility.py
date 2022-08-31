import random
import numpy as np
import matplotlib.pyplot as plt
import copy
from random import shuffle

# Translate a profile pf utility into  Borda utilities
def to_order(utilities):
	res = []
	for u in utilities:
		u = list(u)
		tmp = []
		v = copy.deepcopy(u)
		v.sort()
		for i in v:
			tmp.append(u.index(i))
		res.append(tmp)
	return res

# Build single-peaked preferences => Je pense qu'il y a plein de biais statistique dans ce que fais
def single_peaked(n, maximum):
	res = np.zeros(n)
	index_max = random.randint(0, n - 1)  # index du top
	res[0] = random.randint(n, maximum)
	for i in range(1, n):
		if i <= index_max:
			# On doit laisser assez de place pour les suivants
			res[i] = random.randint(res[i - 1] + 1, n + maximum - (index_max - i)) 
		else:
			res[i] = random.randint(n - i, res[i - 1] - 1)
	return res

# Build single-peaked preferences with uniform pick=> (method of  Conitzer)
def single_peaked_UP(n):
	res = np.zeros(n)
	val = n
	index_max = random.randint(0, n - 1)  # index du top
	res[index_max] = val
	val = val -1
	index_left = index_max -1
	index_right = index_max +1
	while index_left >= 0 and index_right < n :
		r = random.randint(0,1)
		if r:
			res[index_left] = val
			index_left = index_left -1
		else :
			res[index_right] = val
			index_right = index_right +1
		val = val -1

	while index_left >=0 :
		res[index_left] = val
		index_left = index_left - 1
		val = val-1

	while index_right < n :
		res[index_right] = val
		index_right = index_right + 1
		val = val - 1

	return res

# # Build single-peaked preferences recursively => method by T.  Walsh)
def single_peaked_IP(n):
	res = np.zeros(n)
	index_left = 0
	index_right = n-1
	val = 1
	while val <= n:
		r = random.randint(0, 1)
		if r:
			res[index_left] = val
			index_left = index_left +1
		else:
			res[index_right] = val
			index_right = index_right -1
		val = val +1
	return res



# Single-peaked  with possible indiferences
def single_peaked_indif(n, maximum):
	res = np.zeros(n)
	index_max = random.randint(0, n - 1)
	res[0] = random.randint(n, maximum)
	for i in range(1, n):
		if i <= index_max:
			res[i] = random.randint(res[i - 1], n + maximum - (index_max - i))
		else:
			res[i] = random.randint(n - i, res[i - 1])
	return res

# random utilities
def random_u(n, maximum):
	res = np.zeros(n)
	for i in range(n):
		res[i] = random.randint(n, maximum)
	return res

# Retourne les fonctions d'utilite (utilities est un profil) restreinte aux ressources => on peut ameliorer avec np.where
def restrict(utilities, resources):
	res = []
	for u in utilities:
		tmp = []
		for r in resources:
			tmp.append(u[r])
		res.append(tmp)
	return res

# Retourne les argmin pour chacune des restrictions
def argmin_restrict(resources, utilities):
	tmp = restrict(utilities, resources)
	res = []
	for u in tmp:
		m = min(u)	
		for r in range(len(resources)):
			if u[r] == m and resources[r] not in res:
				res.append(resources[r])
	return res

# Truc bizare dans l'algo pour tester si des preferences sont single-peaked on a tree => voir l'article de Dominik et Edith
# dans Trends in COMSOC
def interB(utilities, resources, r):
	restrict_u = restrict(utilities, resources)
	res = []
	for u in restrict_u:
		u = np.array(u)
		if np.argmax(u) == r:
			tmp = [u.argsort()[-2]]
		else:
			tmp = np.where(u > u[resources.index(r)])[0]
		res.append(set(tmp))
	tmp = set(res[0])
	for s in res:
		tmp = s.intersection(tmp)
	return list(tmp)

# Remove an element from l
def rec_remove(l, remov):
	res = copy.deepcopy(l)
	for r in remov:
		res.remove(r)
	return res

# Attachement digraph pour tester si des preferences sont single-peaked on a tree => voir l'article de Dominik et Edith
# dans Trends in COMSOC
def attachement_digraph(utilities):
	resources = list(range(len(utilities[0])))
	A = []
	resources_prime = resources
	while len(resources_prime) >= 3:
		minR = argmin_restrict(resources_prime, utilities)
		for r in minR:
			B = interB(utilities, resources_prime, r)
			if B == []:
				return None
			else:
				for r2 in B:
					if (r, r2) not in A:
						A.append((r, r2))
		resources_prime = rec_remove (resources_prime, minR)
	return (resources, A)


def rand_unif(nbresources, max):
	res = np.arange(1,max+1)
	np.random.shuffle(res)
	return res


# Build a single-peaked profile for all the agents
def generate_SP(nb_player, nb_resources):
	return [single_peaked(nb_resources, nb_resources * 10) for i in range(nb_player)]

# Build a single-peaked UP profile for all the agents
def generate_SP_UP(nb_player, nb_resources):
	return [single_peaked_UP(nb_resources) for i in range(nb_player)]

# Build a single-peaked profile IC for all the agents
def generate_SP_IP(nb_player, nb_resources):
	return [single_peaked_IP(nb_resources) for i in range(nb_player)]


# Build a single-peaked profile with indiferences for all the agents
def generate_SP_indif(nb_player, nb_resources):
	return [single_peaked_indif(nb_resources, nb_resources * 5) for i in range(nb_player)]


def generate_rand_unif(nbplayer, nbresources,  max):
	return [rand_unif(nbresources, max) for i in range(nbplayer)]

def generate_borda_diff(nbplayer, nbresources):
	allPrefList = []
	for i in range(nbplayer):
		prefList = [i for i in range (1, nbresources+1)]
		random.shuffle(prefList)
		allPrefList.append(prefList)
	return allPrefList

# Build a single-peaked profile for n-1 agents SP and 1 non SP
def generate_mixt(nb_player, nb_resources):
	tmp = generate_SP(nb_player - 1, nb_resources)
	t = generate_SP(1, nb_resources)[0]
	np.random.shuffle(t)
	tmp.append(t)
	return tmp

# Test si une alloc est sequencable par restriction successive et test de la non-frustration
def is_sequenceable(players):
	players = copy.deepcopy(players)
	seq = []
	pref = [p.SP for p in players]
	alloc = [p.bundle for p in players]
	for i in range(len(pref[0])):
		max_p = -1
		for j in range(len(pref)):
			max_r = np.argmax(pref[j])
			if max_r in alloc[j]:
				max_p = j
				seq.append(j)
				for k in range(len(pref)):
					pref[k][max_r] = -1
				break
		if max_p == -1:
			return []
	return seq

# Return the value of a bundle with additive preferences
def additive(bundle, SP):
	res = 0
	for b in bundle:
		res += SP[b]
	return res

#Return the value of a bundle with max preferences
def maxi(bundle, SP):
	return max([SP[b] for b in bundle])

#Return the value of a bundle with min preferences
def mini(bundle, SP):
	return min([SP[b] for b in bundle])



#Return SWU and SWE of an allocation
def evalAlloc(alloc, pref, nbAg, verbose=False):
	swU = 0
	swE = -1
	if(verbose) :
		print("alloc a evaluer :", alloc)
	for i in range (0, nbAg):
		utiAg = 0
		allocAg = alloc[i]
		prefAg = pref[i]
		for e in allocAg :
			utiAg = prefAg[e]
			swU = swU + utiAg
			if (verbose):
				print("agent", i, " ->" , e, " uti = ", utiAg, " sum = ", swU  )
		if (swE == -1 or utiAg < swE) :
			swE = utiAg
	return  swU, swE




# Plot pereferences in a graphic
def plot_u(utility):
	plt.close('all')
	plt.figure()
	plt.plot(utility)
	plt.show()
	plt.close()

def test():
	print("hello")