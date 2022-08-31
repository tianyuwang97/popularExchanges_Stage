

#record the outcomes of the different dynamics for a MARA instance
class Test_instance(object):

# num : id of the run, initial : initial allocation, pref: preferences of the agents
    def __init__(self, num, initial, pref):
        self.num = num
        self.initial = initial
        self.pref  = pref
        self.outcomes = dict()

#dyn : dynamics of the exchanges, final : final allocation
    def add_outcome(self, dyn, final):
        self.outcomes[dyn]  = final

    def printOutcomes(self):
        res = "\n"
        for i in self.outcomes.keys():
            res = res + "\t \t metho  " + i + " -> ["
            for j in self.outcomes[i]:
               res = res+ str(j) + ","
            res = res + "]\n"
        return res

    def __str__(self):
        return   str(self.num) + "\n\tInitial: " + str(self.initial) + "\n\tpref: " + str(self.pref) +"\n\toutcome: " + self.printOutcomes() + "\n"

