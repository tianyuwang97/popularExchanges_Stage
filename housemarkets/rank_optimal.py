#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:42:14 2019

@author: nicolas
"""

import pulp
import random
#from housemarkets import allocTools, player,swap, utility
import allocTools, player,swap, utility
import numpy as np



###############################################################################
# Max utilitarian (average rank) assignment as a MIP (2 versions: assuming Individual Rational deals or not)
###############################################################################


def maxUtilitarianIR(initial,preferences,verbose=False, epsilon = 0.1):
    '''
    @init the initial allocation
    @preferences agents preferences
    '''
    
    nb_resources = sum([len(i) for i in initial])
    
    agents = list(range(0,len(preferences))) 
    resources = list(range(0,nb_resources))
        
    # building the pulp model    
    
    maxAvgRankMIP = pulp.LpProblem("Max utilitarian assignement",pulp.LpMaximize)

    # creating the variables

    x = pulp.LpVariable.dicts("assignement", (agents, resources),cat = pulp.LpBinary)

    # objective function: maximize 
    
    maxAvgRankMIP += sum([preferences[i][j]*x[i][j] for i in agents for j in resources]) 
    
    # each resource assigned to exactly one agent and each agent gets one resource
    for j in resources: 
        maxAvgRankMIP += sum([x[i][j] for i in agents])==1
    for i in agents: 
        maxAvgRankMIP += sum([x[i][j] for j in resources]) == 1
    
        
    # IR constraint: utility of each agent must be higher than her initial item
    for i in agents:
        maxAvgRankMIP += sum([preferences[i][j]*x[i][j] for j in resources])>= preferences[i][initial[i]]

        
    # solving and printing

    #maxAvgRankMIP.solve()
    maxAvgRankMIP.solve(pulp.GUROBI())

    alloc_finale = [[j] for i in agents for j in resources if x[i][j].varValue > 1- epsilon]
    if verbose:      
         print(alloc_finale)
         print(pulp.value(maxAvgRankMIP.objective))
    return alloc_finale


def maxUtilitarian(initial, preferences, verbose=False, epsilon = 0.1):
    '''
    @init the initial allocation
    @preferences agents preferences
    '''

    nb_resources = sum([len(i) for i in initial])

    agents = list(range(0, len(preferences)))
    resources = list(range(0, nb_resources))

    if(verbose):
      print("initiale : ", initial)

    # building the pulp model

    maxAvgRankMIP = pulp.LpProblem("Max utilitarian assignement", pulp.LpMaximize)

    # creating the variables

    x = pulp.LpVariable.dicts("assignement", (agents, resources), cat=pulp.LpBinary)

    # objective function: maximize

    maxAvgRankMIP += sum([preferences[i][j] * x[i][j] for i in agents for j in resources])

    # each resource assigned to exactly one agent
    for j in resources:
        maxAvgRankMIP += sum([x[i][j] for i in agents]) == 1
    for i in agents: 
        maxAvgRankMIP += sum([x[i][j] for j in resources]) == 1
    

        # IR constraint: utility of each agent must be higher than her initial item
    #for i in agents:
    #   maxAvgRankMIP += sum([preferences[i][j] * x[i][j] for j in resources]) >= preferences[i][initial[i]]

    # solving and printing

    #maxAvgRankMIP.solve()
    maxAvgRankMIP.solve(pulp.GUROBI())

    alloc_finale = [[j] for i in agents for j in resources if x[i][j].varValue > 1- epsilon]
    if verbose:
        print("finale : ",alloc_finale)
        print ("value : ",pulp.value(maxAvgRankMIP.objective))
    return alloc_finale


###############################################################################
# Max egalitarian (maxmin rank) assignment as a MIP (2 versions: assuming Individual Rational deals or not)
###############################################################################


def maxEgalitarianIR(initial,preferences,verbose=False,epsilon = 0.1):
    '''
    @init the initial allocation
    @preferences agents preferences
    '''
    
    nb_resources = sum([len(i) for i in initial])
    
    agents = list(range(0,len(preferences))) 
    resources = list(range(0,nb_resources))
        
    # building the pulp model    
    
    maxMinRankMIP = pulp.LpProblem("Max utilitarian assignement",pulp.LpMaximize)

    # creating the variables

    x = pulp.LpVariable.dicts("assignement", (agents, resources),cat = pulp.LpBinary)
    k = pulp.LpVariable("bound", lowBound = 0)

    # objective function: maximize k
    
    maxMinRankMIP += k
    
    # each resource assigned to exactly one agent
    for j in resources: 
        maxMinRankMIP += sum([x[i][j] for i in agents]) == 1
    for i in agents: 
        maxMinRankMIP += sum([x[i][j] for j in resources]) == 1
    
        
    # IR constraint: utility of each agent must be higher than her initial item
    for i in agents:
        maxMinRankMIP += sum([preferences[i][j]*x[i][j] for j in resources])>= preferences[i][initial[i]]
        
    # utility of each agent must be higher than bound k
    for i in agents:
        maxMinRankMIP += sum([preferences[i][j]*x[i][j] for j in resources])>= k
        
        
    # solving and printing

    #maxMinRankMIP.solve()
    maxMinRankMIP.solve(pulp.GUROBI())

    alloc_finale = [[j] for i in agents for j in resources if x[i][j].varValue > 1- epsilon]
    if verbose:
        print(alloc_finale)
    #return pulp.value(maxMinRankMIP.objective)
    return alloc_finale


def maxEgalitarian(initial, preferences, verbose=False, epsilon = 0.1):
    '''
    @init the initial allocation
    @preferences agents preferences
    '''

    nb_resources = sum([len(i) for i in initial])

    agents = list(range(0, len(preferences)))
    resources = list(range(0, nb_resources))

    # building the pulp model

    maxMinRankMIP = pulp.LpProblem("Max utilitarian assignement", pulp.LpMaximize)

    # creating the variables

    x = pulp.LpVariable.dicts("assignement", (agents, resources), cat=pulp.LpBinary)
    k = pulp.LpVariable("bound", lowBound=0)

    # objective function: maximize k

    maxMinRankMIP += k

    # each resource assigned to exactly one agent
    for j in resources:
        maxMinRankMIP += sum([x[i][j] for i in agents]) == 1
    for i in agents: 
        maxMinRankMIP += sum([x[i][j] for j in resources]) == 1
    


    # utility of each agent must be higher than bound k
    for i in agents:
        maxMinRankMIP += sum([preferences[i][j] * x[i][j] for j in resources]) >= k

    # solving and printing

    #maxMinRankMIP.solve()
    maxMinRankMIP.solve(pulp.GUROBI())
    #if verbose :
     #   for v in maxMinRankMIP.variables():
      #      print(v.name, "=", v.varValue)

    alloc_finale = [[j] for i in agents for j in resources if x[i][j].varValue > 1- epsilon]
    if verbose:
        print(alloc_finale)
        #print pulp.value(maxMinRankMIP.objective)
    return alloc_finale



if __name__ == "__main__":
### Testing
# #
    #nb_players = 6
    #nb_resources = 6
    #allocs = allocTools.all_even_sized_alloc(nb_resources, 1)
    #init = allocs[random.randint(0, nb_players)]
    #print("Allocation initiale : {}".format(init))
    #preferences = utility.generate_SP_UP(nb_players, nb_players)
    #print("Preferences = ", preferences)
# # #
# # #
#     print(maxUtilitarian(init,preferences,True))
#     print(maxEgalitarian(init,preferences,True))

    nb_players = 5
    nb_resources = 5
    init = [[2], [3], [1],[4], [0]]
    print("Allocation initiale : {}".format(init))
    preferences = [np.array([1.0, 2.0, 4.0, 5.0, 3.0]), np.array([3.0, 4.0, 5.0, 2.0, 1.0]), np.array([3.0, 4.0, 5.0, 2.0, 1.0]), np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array([3.0, 5.0, 4.0, 2.0, 1.0])]

    print("Preferences = ", preferences)
# #
# #
    print("max Uti IR",maxUtilitarianIR(init,preferences,True))
    print("max Uti", maxUtilitarian(init,preferences,True))

    init = [[4], [3], [1],[0], [2]]
    print("Allocation initiale : {}".format(init))
    preferences = [np.array([1.0, 5.0, 4.0, 3.0, 2.0]), np.array([2.0, 4.0, 5.0, 3.0, 1.0]), np.array([3.0, 5.0, 4.0, 2.0, 1.0]), np.array([2.0, 3.0, 4.0, 5.0, 1.0]), np.array([1.0, 2.0, 5.0, 4.0, 3.0])]

    print("Preferences = ", preferences)
# #
# #
    print("max Uti IR", maxUtilitarianIR(init,preferences,True))
    print("*******")
    print("max Uti", maxUtilitarian(init,preferences,True))


    nb_players = 8
    nb_resources = 8
    init = [[7], [2], [0], [4], [1], [3], [6], [5]]
    print("Allocation initiale : {}".format(init))
    preferences = [np.array([8., 7., 6., 5., 4., 3., 2., 1.]), np.array([1., 2., 3., 4., 7., 8., 6., 5.]), np.array([1., 2., 3., 4., 5., 6., 8., 7.]), np.array([1., 2., 3., 4., 5., 8., 7., 6.]), np.array([1., 2., 3., 4., 5., 7., 8., 6.]), np.array([1., 2., 3., 4., 5., 8., 7., 6.]), np.array([1., 3., 4., 6., 8., 7., 5., 2.]), np.array([6., 8., 7., 5., 4., 3., 2., 1.])]
    print("Preferences = ", preferences)
# #
# #
    print("max Uti IR", maxUtilitarianIR(init,preferences,True))

    print("max Egal",maxEgalitarian(init,preferences,True))




