__author__ = 'Konrad Kopciuch'

from GapPenalties import get_penalties_dictionary

class SCFG:

    def __init__(self, states, single_scoring_matrix, double_scoring_matrix):
        self.states = []
        self.gap_penalties = get_penalties_dictionary(1,2) #TODO: prawdziwe wartosci

