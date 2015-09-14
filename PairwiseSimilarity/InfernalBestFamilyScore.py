__author__ = 'Konrad Kopciuch'

from Infernal.Infernal import Infernal
from Config import Config
from Repository.MongoInfernalRepository import MongoInfernalRepository

class InfernalBestFamilyScore:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        config = Config('config.ini')
        cmscan_path = config.get_infernal_cmscan()
        cmdatabase_path = config.get_infernal_cmdatabase()
        infernal = Infernal(cmscan_path, cmdatabase_path)

        query_families = infernal.get_families_for_sequence(query_sequence)
        repo = MongoInfernalRepository()
        scores = [0]
        for (template_rfam_id, template_rfam_name, template_score) in repo.get_families_for_template(template_id):
            for (query_rfam_name, query_score) in query_families:
                if template_rfam_name == query_rfam_name:
                    assert template_score !=0
                    assert query_score != 0
                    value = min(template_score/query_score, query_score/template_score)
                    scores.append(value)
        return max(scores)