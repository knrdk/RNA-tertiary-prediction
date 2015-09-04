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
        n_states = len(self.states)
        n_sequence = len(sequence)
        self.alpha = self.__get_3D_array(n_states, n_sequence+1, n_sequence+1)
        return self.CYK_Inside(0, n_sequence-1, 0, n_sequence-1)

    def get_transition_cost(self, begin_state, end_state):
        begin_class = begin_state.get_gap_class()
        end_class = end_state.get_gap_class()
        return (-1) * self.gap_penalties[begin_class][end_class]

    def CYK_Inside(self, r, z, g, q):
        for v in range(z, r-1, -1):
            for j in range(g-1, q+1, 1):
                for i in range(j+1, g-1, -1):
                    d = j-i+1
                    state = self.states[v]
                    state_type = state.state_type
                    if state_type in {StateTypes.D, StateTypes.S}:
                        min = float("inf")
                        for connected in state.get_connected_indexes():
                            connected_state = self.states[connected]
                            transition_cost = self.get_transition_cost(state, connected_state)
                            if transition_cost < min:
                                min = transition_cost
                        print transition_cost
                    elif state_type == StateTypes.P and d>=2:
                        pass
                    elif state_type == StateTypes.L and d>=1:
                        pass
                    elif state_type == StateTypes.R and d>=1:
                        pass
                    elif state_type == StateTypes.B:
                        pass
                    elif state_type == StateTypes.E and d == 0:
                        pass
                    else:
                        pass
                        #print v, i, j
                        #self.alpha[v][i][j] = float("-inf")

    def __get_3D_array(self, depth, width, height):
        return [self.__get_2D_array(width, height) for x in range(depth)]

    def __get_2D_array(self, width, height):
        return [[0 for x in range(width)] for x in range(height)]