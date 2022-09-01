
class PreflibInstance(object):
	def __init__(self):
		self.fileName = ""
		self.nbAlternatives = 0
		self.alternativesName = {}
		self.nbOrders = 0
		self.nbDifferentOrders = 0
		self.nbEachOrder = []
		self.orders = []

	def parseSO(self, fileName):
		self.fileName = fileName
		file = open(self.fileName, "r", encoding="utf-8")
		res = []
		lines = file.readlines()
		self.nbAlternatives = int(lines[0])
		for i in range(1, self.nbAlternatives + 1):
			self.alternativesName[i] = lines[i].split(",")[1].strip()
		self.nbOrders = int(lines[self.nbAlternatives + 1].split(",")[0])
		self.nbDifferentOrders = int(lines[self.nbAlternatives + 1].split(",")[2])
		# Skip the lines that describes the data
		for l in lines[self.nbAlternatives + 2:]:
			pref = []
			weights = l.split(",")
			# Skip the first value
			self.nbEachOrder.append(int(weights[0]))
			for w in weights[1:]:
				if int(w) - 1 not in pref:
					pref.append(int(w) - 1)
			self.orders.append(pref)
		file.close()

	def getRestrictionInstance(self, agentSet, alternativesSet):
		print("Restricting {} to agents {} and resources {}".format(self.fileName, agentSet, alternativesSet))
		res = PreflibInstance()
		res.fileName = self.fileName

		res.nbAlternatives = len(alternativesSet)
		for a in alternativesSet:
			res.alternativesName[a + 1] = self.alternativesName[a + 1]

		countEachOrder = {}
		for a in agentSet:
			newOrder = []
			for r in self.orders[a]:
				if r in alternativesSet:
					newOrder.append(r)
			if str(newOrder) in countEachOrder:
				countEachOrder[str(newOrder)] += self.nbEachOrder[a]
			else:
				countEachOrder[str(newOrder)] = self.nbEachOrder[a]
			res.orders.append(newOrder)
			res.nbEachOrder.append(self.nbEachOrder[a])

		# We remove duplicates orders and update the number of orders accordingly
		res.orders = list(set([tuple(o) for o in res.orders]))
		res.orders = [list(o) for o in res.orders]
		res.nbEachOrder = []
		for o in res.orders:
			res.nbEachOrder.append(countEachOrder[str(o)])

		res.nbDifferentOrders = len(res.orders)
		res.nbOrders = sum(res.nbEachOrder)

		print("Final instance " + str(res))
		return res

	def write(self, fileName):
		outFile = open(fileName, "w", encoding = "utf-8")
		outFile.write(str(self.nbAlternatives) + "\n")
		for (a, name) in self.alternativesName.items():
			outFile.write(str(a) + "," + str(name) + "\n")
		outFile.write(str(self.nbOrders) + "," + str(self.nbOrders) + "," + str(self.nbDifferentOrders) + "\n")
		for i in range(len(self.orders)):
			outFile.write(str(self.nbEachOrder[i]))
			for w in self.orders[i]:
				outFile.write("," + str(w + 1))
			outFile.write("\n")
		outFile.close()
		print("Instance written in " + str(fileName))

	def __str__(self):
		res = "Instance " + str(self.fileName) + "\n"
		res += str(self.nbAlternatives) + " alternatives :\n"
		for (a, name) in self.alternativesName.items():
			res += "\t" + str(a) + " : " + str(name) + "\n"
		res += str(self.nbOrders) + " orders (" + str(self.nbDifferentOrders) + " different) :\n"
		for i in range(len(self.orders)):
			res += "\t" + str(self.nbEachOrder[i]) + " times : " + str(self.orders[i]) + "\n"
		return res[:-1]

	def __repr__(self):
		return str(self)

# p = PreflibInstance()
# p.parseSO("../DataPrefLib/allSOC/ED-00015-00000077.soc")
# p.parseSO("../DataPrefLib/allSOI/ED-00001-00000001.soi")
# p.parseSO("../allSOI/ED-00011-00000070.soi")
# p.parseSO("../../DataPrefLib/allSOC/ED-00004-00000028.soc")
# print(p)
