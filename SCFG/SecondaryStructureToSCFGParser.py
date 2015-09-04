__author__ = 'Konrad Kopciuch'

from SecondaryStructureToNodesTreeParser import SecondaryStructureToNodesTreeParser
from SCFG import SCFG

class SecondaryStructureToSCFGParser:

    def __init__(self, single_scoring_matrix, double_scoring_matrix):
        self.single_matrix = single_scoring_matrix
        self.double_matrix = double_scoring_matrix

    def get_SCFG(self, secondary_structure, sequence):
        parser = SecondaryStructureToNodesTreeParser()
        tree = parser.get_tree(secondary_structure, sequence)
        print tree.get_number_of_states()
        states = tree.get_states()

        for index, state in enumerate(states):
            state.set_index(index)

        return SCFG(states, self.single_matrix, self.double_matrix)