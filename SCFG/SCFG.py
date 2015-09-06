__author__ = 'Konrad Kopciuch'

from GapPenalties import get_penalties_dictionary
from States import StateTypes

class SCFG:

    def __init__(self, states, single_scoring_matrix, double_scoring_matrix):
        self.states = states
        self.gap_penalties = get_penalties_dictionary(1,2) #TODO: prawdziwe wartosci
        self.single_matrix = single_scoring_matrix
        self.double_matrix = double_scoring_matrix

    def get_score(self):
        score = self.alpha[0][0][len(self.sequence) - 1]
        return score

    def align(self, sequence):
        self.sequence = sequence
        states_length = len(self.states)
        sequence_length = len(sequence)
        self.alpha = self.__get_3D_array(states_length, sequence_length+1, sequence_length+1)
        self.tau = self.__get_3D_array(states_length, sequence_length+1, sequence_length+1)
        self.__CYK_Inside(0, states_length-1, 0, sequence_length-1)

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
                    maximum, index_max = float("-inf"), -1

                    if state_type in {StateTypes.D, StateTypes.S}:
                        maximum, index_max = float("-inf"), -1
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i][j]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > maximum:
                                maximum, index_max = value, gamma
                    elif state_type == StateTypes.P and d>=2:
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i+1][j-1]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > maximum:
                                maximum, index_max = value, gamma
                        base_pair = self.sequence[i] + self.sequence[j]
                        emission_cost = self.get_double_emission_cost(state, base_pair)
                        maximum = maximum + emission_cost
                    elif state_type == StateTypes.L and d>=1:
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i+1][j]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > maximum:
                                maximum, index_max = value, gamma
                        emission_cost = self.get_single_emission_cost(state, self.sequence[i])
                        maximum = maximum + emission_cost
                    elif state_type == StateTypes.R and d>=1:
                        for gamma in state.get_connected_indexes():
                            gamma_value = self.alpha[gamma][i][j-1]
                            transition_cost = self.get_transition_cost(state, self.states[gamma])
                            value = gamma_value + transition_cost
                            if value > maximum:
                                maximum, index_max = value, gamma
                        emission_cost = self.get_single_emission_cost(state, self.sequence[j])
                        maximum = maximum + emission_cost
                    elif state_type == StateTypes.B:
                        left, right = state.get_connected_indexes()
                        for k in range(i,j,1):
                            left_value = self.alpha[left][i][k]
                            right_value = self.alpha[right][k+1][j]
                            value = left_value + right_value
                            if value > maximum:
                                maximum, index_max = value, k
                    elif state_type == StateTypes.E and d == 0:
                        maximum = 0

                    self.alpha[v][i][j] = maximum
                    self.tau[v][i][j] = index_max

    def __get_3D_array(self, depth, width, height):
        return [self.__get_2D_array(width, height) for x in range(depth)]

    def __get_2D_array(self, width, height):
        return [[None for x in range(width)] for x in range(height)]