__author__ = 'Konrad Kopciuch'

from GapPenalties import get_penalties_dictionary
from Nodes import *

class SCFG:

    def __init__(self, states, single_scoring_matrix, double_scoring_matrix):
        self.states = states
        self.gap_penalties = get_penalties_dictionary(1,2) #TODO: prawdziwe wartosci
        self.single_matrix = single_scoring_matrix
        self.double_matrix = double_scoring_matrix

    def align(self, sequence):
        self.sequence = sequence
        states_length = len(self.states)
        sequence_length = len(sequence)
        self.alpha = self.__get_3D_array(states_length, sequence_length+1, sequence_length+1)
        self.tau = self.__get_3D_array(states_length, sequence_length+1, sequence_length+1)
        self.__CYK_Inside(0, states_length-1, 0, sequence_length-1)

    def get_score(self):
        score = self.alpha[0][0][len(self.sequence) - 1]
        return score

    def get_alingment(self):
        states = []
        self.__Traceback(0, 0, len(self.sequence)-1, states) #wypelnia states stanami dla dopasowania self.sequence

        return self.__get_alingment_from_states(states)

    def __get_alingment_from_states(self, states):
        template_left, template_right = '', ''
        query_left, query_right = '', ''
        while len(states) > 0:
            x = states.pop(0)
            state = x[0]
            state_type = state.state_type
            parent_node = state.parent_node
            print state, parent_node.__class__.__name__
            if isinstance(state, D):
                if isinstance(parent_node, MATP):
                    template_left += parent_node.nucleotide1
                    template_right += parent_node.nucleotide2
                    query_left += '-'
                    query_right += '-'
                elif isinstance(parent_node, MATL):
                    template_left += parent_node.nucleotide
                    query_left += '-'
                elif isinstance(parent_node, MATR):
                    template_right += parent_node.nucleotide
                    query_right += '-'
            elif isinstance(state, MP):
                template_left += parent_node.nucleotide1
                template_right += parent_node.nucleotide2
                query_left += x[1]
                query_right += x[2]
            elif isinstance(state, ML):
                if isinstance(parent_node, MATP):
                    template_left += parent_node.nucleotide1
                    template_right += parent_node.nucleotide2
                    query_left += x[1]
                    query_right += '-'
                elif isinstance(parent_node, MATL):
                    template_left += parent_node.nucleotide
                    query_left += x[1]
            elif isinstance(state, MR):
                if isinstance(parent_node, MATP):
                    template_left += parent_node.nucleotide1
                    template_right += parent_node.nucleotide2
                    query_left += '-'
                    query_right += x[1]
                elif isinstance(parent_node, MATR):
                    template_right += parent_node.nucleotide
                    query_right += x[1]
            elif isinstance(state, IL):
                template_left += '-'
                query_left += x[1]
            elif isinstance(state, IR):
                template_right += '-'
                query_right += x[1]
            elif isinstance(state, B):
                left, right = self.split_states_in_bifurcation(states)
                l_t, l_q = self.__get_alingment_from_states(left)
                r_t, r_q = self.__get_alingment_from_states(right)
                template_left = template_left + l_t
                template_right = r_t + template_right
                query_left = query_left + l_q
                query_right = r_q + query_right

        template = template_left + template_right
        query = query_left + query_right
        return template, query

    def split_states_in_bifurcation(self, states):
        left = []
        while True:
            x = states.pop(0)
            left.append(x)
            if isinstance(x[0], E):
                break
        return left, states


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
        minus_inf = float("-inf")
        for v in range(z, r-1, -1):
            for j in range(g-1, q+1, 1):
                for i in range(j+1, g-1, -1):
                    d = j-i+1
                    state = self.states[v]
                    state_type = state.state_type
                    maximum, index_max = minus_inf, -1

                    if state_type == StateTypes.D or state_type == StateTypes.S:
                        maximum, index_max = minus_inf, -1
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

    def __Traceback(self, v, i, j, list_of_states):
        state = self.states[v]
        state_type = state.state_type

        if state_type == StateTypes.E:
            list_of_states.append((self.states[v], None, None))
        elif state_type == StateTypes.S or state_type == StateTypes.D:
            list_of_states.append((self.states[v], None, None))
            self.__Traceback(self.tau[v][i][j], i, j, list_of_states)
        elif state_type == StateTypes.P:
            list_of_states.append((self.states[v], self.sequence[i], self.sequence[j]))
            self.__Traceback(self.tau[v][i][j], i+1, j-1, list_of_states)
        elif state_type == StateTypes.L:
            list_of_states.append((self.states[v], self.sequence[i], None))
            self.__Traceback(self.tau[v][i][j], i+1, j, list_of_states)
        elif state_type == StateTypes.R:
            list_of_states.append((self.states[v], self.sequence[j], None))
            self.__Traceback(self.tau[v][i][j], i, j-1, list_of_states)
        elif state_type == StateTypes.B:
            left, right = state.get_connected_indexes()
            list_of_states.append((self.states[v], None, None))
            self.__Traceback(left, i, self.tau[v][i][j], list_of_states)
            self.__Traceback(right, self.tau[v][i][j] + 1, j, list_of_states)

    def __get_3D_array(self, depth, width, height):
        return [self.__get_2D_array(width, height) for x in range(depth)]

    def __get_2D_array(self, width, height):
        return [[None for x in range(width)] for x in range(height)]