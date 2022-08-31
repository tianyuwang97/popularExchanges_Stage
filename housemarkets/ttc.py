#from housemarkets.graph import *

import graph

# getAgents: graph, vertex -> set(vertex)
# get the set of agents on a cycle starting at the given vertex
def getAgents(G, cycle, agents):
   # a cycle in G is represented by any vertex of the cycle
   # outdegree guarantee means we don't care which vertex it is

   # make sure starting vertex is a house
   if cycle.vertexId in agents:
      cycle = cycle.anyNext()

   startingHouse = cycle
   currentVertex = startingHouse.anyNext()
   theAgents = set()

   while currentVertex not in theAgents:
      theAgents.add(currentVertex)
      currentVertex = currentVertex.anyNext()
      currentVertex = currentVertex.anyNext()

   return theAgents


# anyCycle: graph -> vertex
# find any vertex involved in a cycle
def anyCycle(G):
   visited = set()
   v = G.anyVertex()

   while v not in visited:
      visited.add(v)
      v = v.anyNext()

   return v


# find a core matching of agents to houses
# agents and houses are unique identifiers for the agents and houses involved
# agentPreferences is a dictionary with keys being agents and values being
# lists that are permutations of the list of all houses.
# initiailOwnerships is a dict {houses:agents}
def topTradingCycles(agents, houses, agentPreferences, initialOwnership):
   # form the initial graph
   agents = set(agents)
   vertexSet = set(agents) | set(houses)
   G = graph.Graph(vertexSet)
   nbCycles = 0
   nbSwap = 0
   sizeCycle = 0
   maxSizeC = -1
   minSizeC = -1

   # maps agent to an index of the list agentPreferences[agent]
   currentPreferenceIndex = dict((a,0) for a in agents)
   preferredHouse = lambda a: agentPreferences[a][currentPreferenceIndex[a]]

  # print("pref=", agentPreferences)
   #print("init alloc", initialOwnership)

   for a in agents:
      G.addEdge(a, preferredHouse(a))
      #print("pref", a, "->", preferredHouse(a))
   for h in houses:
      G.addEdge(h, initialOwnership[h])

   # iteratively remove top trading cycles
   allocation = dict()
   while len(G.vertices) > 0:
      cycle = anyCycle(G)
      cycleAgents = getAgents(G, cycle, agents)
      #print("cycle :",cycleAgents)
      if(cycleAgents.__len__() > 1):
         nbCycles = nbCycles +1
         sizeC = cycleAgents.__len__()
         sizeCycle = sizeCycle+ sizeC
         nbSwap = nbSwap + sizeC -1
         if (minSizeC == -1 or sizeC < minSizeC):
            minSizeC = sizeC
         if (maxSizeC == -1 or sizeC > maxSizeC):
            maxSizeC = sizeC


      # assign agents in the cycle their house
      for a in cycleAgents:
         h = a.anyNext().vertexId
         allocation[a.vertexId] = h
         G.delete(a)
         G.delete(h)

      for a in agents:
         if a in G.vertices and G[a].outdegree() == 0:
            while preferredHouse(a) not in G.vertices:
               currentPreferenceIndex[a] += 1
            G.addEdge(a, preferredHouse(a))

   return (allocation, sizeCycle, nbCycles,minSizeC,maxSizeC,nbSwap)


def our_format_ttc(nbAgents, preferences, init): # run ttc with our input / output format
   agents = set()
   resources = set()
   pref = dict()
   initDict = dict()

   for i in range(0, nbAgents):
      agents.add(str(i))
      resources.add(i)
      prefI = preferences[i]
      prefBis = [0 for e in range(nbAgents)]
      for k in range(1, nbAgents+1):
         j = 0
         while (j< nbAgents) and (int(prefI[j])!=k) :
            j = j+1
         prefBis[nbAgents-k] = j

      pref[str(i)] = prefBis
      lInit = init[i]
      initDict[lInit[0]] = str(i)


   res, size, nbC, minC, maxC,nbSwap = topTradingCycles(agents,resources,pref, initDict)

   newRes = [-1]*nbAgents
   for i in range(0,nbAgents):
      newRes[i] = [res[str(i)]]

   if(nbC !=0):
      size = size / nbC
   #print(newRes)
   return newRes, size, nbC, minC, maxC, nbSwap





if __name__ == "__main__":
   def main():
      print(topTradingCycles({'a','b','c', 'd'},{0,1,2,3},{'a':[0,1,2,3],'b':[3,2,1,0],'c':[1,2,3,0],'d':[2,3,1,0]},{0:'a',1:'b',2:'c',3:'d'}))
      print(topTradingCycles({'0', '1', '2', '3'}, {0, 1, 2, 3},
                           {'0': [0, 1, 2, 3], '1': [3, 2, 1, 0], '2': [1, 2, 3, 0], '3': [2, 3, 1, 0]},
                           {0: '0', 1: '1', 2: '2', 3: '3'}))


   main()