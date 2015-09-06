__author__ = 'rna'

from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices

class SCFGScore:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        single_matrix, double_matrix = get_scoring_matrices()
        parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
        scfg = parser.get_SCFG(template_secondary_structure, template_sequence)

        self_score = scfg.get_score(template_sequence)
        query_score = scfg.get_score(query_sequence)

        if self_score == 0:
            if query_score > 0:
                score = 1
            else:
                score = 0

        score = float(query_score) / self_score
        print score
        return score