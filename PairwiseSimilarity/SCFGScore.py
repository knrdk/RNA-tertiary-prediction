__author__ = 'rna'

from Repository.MongoSCFGRepository import MongoSCFGRepository
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices


class SCFGScore:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        repo = MongoSCFGRepository()

        single_matrix, double_matrix = get_scoring_matrices('config.ini')
        parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
        scfg = parser.get_SCFG(template_secondary_structure, template_sequence)

        self_score = repo.get_scfg_self_score(template_id)

        scfg.align(query_sequence)
        query_score = scfg.get_score()

        if self_score == 0:
            if query_score > 0:
                return 1
            return 0

        score = float(query_score) / self_score
        score = max(score, -1)
        return score
