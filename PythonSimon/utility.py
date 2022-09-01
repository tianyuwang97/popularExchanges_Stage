import random
import numpy as np
import matplotlib.pyplot as plt
import copy
from random import shuffle

# Transforme un profil d'utilité en un profil d'utilité de type Borda
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

# Génère une fonction d'utilité qui est single-peaked => Je pense qu'il y a plein de biais statistique dans ce que fais
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

# Single-peaked avec possiblement des indifférences
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

# Uilité totalement aléatoire
def random_u(n, maximum):
	res = np.zeros(n)
	for i in range(n):
		res[i] = random.randint(n, maximum)
	return res

# Retourne les fonctions d'utilité (utilities est un profil) restreinte aux ressources => on peut améliorer avec np.where
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

# Truc bizare dans l'algo pour tester si des préférences sont single-peaked on a tree => voir l'article de Dominik et Edith
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

# Supprime remov pour tous les éléments de l
def rec_remove(l, remov):
	res = copy.deepcopy(l)
	for r in remov:
		res.remove(r)
	return res

# Attachement digraph pour tester si des préférences sont single-peaked on a tree => voir l'article de Dominik et Edith
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

# Génère un profil Single-peaked pour tous les agents
def generate_SP(nb_player, nb_resources):
	return [single_peaked(nb_resources, nb_resources * 10) for i in range(nb_player)]

# Génère un profil Single-peaked avec possiblement des indifférences pour tous les agents
def generate_SP_indif(nb_player, nb_resources):
	return [single_peaked_indif(nb_resources, nb_resources * 5) for i in range(nb_player)]

# Génère un profil Single-peaked on a tree pour tous les agents => de mémoire ça marche bof (voire pas du tout)
def generate_SPT(nb_player, nb_resources):
	while True:
		tmpu = [random_u(nb_resources, nb_resources * 10) for i in range(nb_player)]
		if attachement_digraph(tmpu) is not None:
			return tmpu

# Génère des préférences avec n-1 agents SP et 1 non SP
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

# Retourne la valeur d'un bundle pour des préférences additives
def additive(bundle, SP):
	res = 0
	for b in bundle:
		res += SP[b]
	return res

# Retourne la valeur d'un bundle pour des préférences max
def maxi(bundle, SP):
	return max([SP[b] for b in bundle])

# Retourne la valeur d'un bundle pour des préférences min
def mini(bundle, SP):
	return min([SP[b] for b in bundle])

# Mal défini, à la limite prendre le max des distances
def distance(bundle, SP):
	res = 0
	for b in bundle:
		res += SP[b]
	if len(bundle) > 1:
		return res + abs(bundle[0] - bundle[1])
	else:
		return res

# Affiche les préférence dans un graphe
def plot_u(utility):
	plt.close('all')
	plt.figure()
	plt.plot(utility)
	plt.show()
	plt.close()