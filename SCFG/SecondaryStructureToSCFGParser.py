__author__ = 'Konrad Kopciuch'

from SecondaryStructureToNodesTreeParser import SecondaryStructureToNodesTreeParser

class SecondaryStructureToSCFGParser:

    def get_SCFG(self, secondary_structure, sequence):
        parser = SecondaryStructureToNodesTreeParser()
        tree = parser.get_tree(secondary_structure, sequence)
        print tree.get_number_of_states()
        states = tree.get_states()

        for index, state in enumerate(states):
            state.set_index(index)

        for state in states:
            print state, list(state.get_connected_indexes())