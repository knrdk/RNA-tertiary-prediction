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
        self.__CYK_Inside(0, n_states-1, 0, n_sequence-1)
        score = self.alpha[0][0][n_sequence - 1]
        return score

    def get_transition_cost(self, begin_state, end_state):
        begin_class = begin_state.get_gap_class()
        end_class = end_state.get_gap_class()
        return (-1) * self.gap_penalties[begin_class][end_class]

    def get_double_emission_cost(self, state, base_pair):
        try:
            return self.double_matrix[state.value][base_pair]
        except:
            return self.double_matrix[base_pair][state.value]


    def get_single_emission_cost(self, state, residuum):
        if not state.value:
            return 0
        try:
            return self.single_matrix[state.value][residuum]
        except:
            return self.single_matrix[residuum][state.value]

    def __CYK_Inside(self, r, z, g, q):
        for v in range(z, r-1, -1):
            for j in range(g-1, q+1, 1):
                for i in range(j+1, g-1, -1):
                    d = j-i+1
                    state = self.states[v]
                    state_type = state.state_type
                    if state_type in {StateTypes.D, StateTypes.S}:
                        max = float("-inf")
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i][j]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > max:
                                max = value
                        self.alpha[v][i][j] = max
                    elif state_type == StateTypes.P and d>=2:
                        base_pair = self.sequence[i] + self.sequence[j]
                        emission_cost = self.get_double_emission_cost(state, base_pair)
                        max = float("-inf")
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i+1][j-1]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > max:
                                max = value
                        self.alpha[v][i][j] = max + emission_cost
                    elif state_type == StateTypes.L and d>=1:
                        emission_cost = self.get_single_emission_cost(state, self.sequence[i])
                        max = float("-inf")
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i+1][j]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > max:
                                max = value
                        self.alpha[v][i][j] = max + emission_cost
                    elif state_type == StateTypes.R and d>=1:
                        emission_cost = self.get_single_emission_cost(state, self.sequence[j])
                        max = float("-inf")
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i][j-1]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > max:
                                max = value
                        self.alpha[v][i][j] = max + emission_cost
                    elif state_type == StateTypes.B:
                        left, right = state.get_connected_indexes()
                        max = float("-inf")
                        for k in range(i,j,1):
                            left_value = self.alpha[left][i][k]
                            right_value = self.alpha[right][k+1][j]
                            value = left_value + right_value
                            if value > max:
                                max = value
                        self.alpha[v][i][j] = max
                    elif state_type == StateTypes.E and d == 0:
                        self.alpha[v][i][j] = 0
                    else:
                        self.alpha[v][i][j] = float("-inf")

    def __get_3D_array(self, depth, width, height):
        return [self.__get_2D_array(width, height) for x in range(depth)]

    def __get_2D_array(self, width, height):
        return [[None for x in range(width)] for x in range(height)]