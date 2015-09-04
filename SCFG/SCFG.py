__author__ = 'Konrad Kopciuch'

from GapPenalties import get_penalties_dictionary
from States import StateTypes

class SCFG:

    def __init__(self, states, single_scoring_matrix, double_scoring_matrix):
        self.states = states
        self.gap_penalties = get_penalties_dictionary(1,2) #TODO: prawdziwe wartosci
        self.single_matrix = single_scoring_matrix
        self.double_matrix = double_scoring_matrix

    def get_score(self, sequence):
        self.sequence = sequence
        return self.CYK_Inside(2,5,3,7)

    def CYK_Inside(self, r, z, g, q):
        for v in range(z, r-1, -1):
            for j in range(g-1, q+1, 1):
                for i in range(j+1, g-1, -1):
                    d = j-i+1
                    state = self.states[v]
                    if state in {StateTypes.D, StateTypes.S}:
                        pass
                    elif state == StateTypes.P and d>=2:
                        pass
                    elif state == StateTypes.L and d>=1:
                        pass
                    elif state == StateTypes.R and d>=1:
                        pass
                    elif state == StateTypes.B:
                        pass
                    elif state == StateTypes.E and d == 0:
                        pass
                    else:
                        pass

