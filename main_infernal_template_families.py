__author__ = 'Konrad Kopciuch'

from Config import Config
import time

from Repository.MongoTemplateRepository import MongoTemplateRepository
from Repository.MongoInfernalRepository import MongoInfernalRepository
from Infernal.Infernal import Infernal
from Infernal.FamilyFileParser import FamilyFileParser


def __get_family_name_rfam_id_mapping(family_file_path):
    parser = FamilyFileParser(family_file_path)
    mapping = parser.get_family_name_rfam_id_mapping()
    return mapping

def main_infernal_template_families(cmscan_path, cmdatabase_path, family_file_path):
    family_name_rfam_id_mapping = __get_family_name_rfam_id_mapping(family_file_path)
    infernal = Infernal(cmscan_path, cmdatabase_path)
    template_repository = MongoTemplateRepository()
    infernal_repository = MongoInfernalRepository()

    for (db_id, sequence, resolution, template_id) in template_repository.get_all_unmodified_sequences():
        families = infernal.get_families_for_sequence(sequence)
        print template_id, families
        if len(families) > 0:
            for (rfam_family_name, score) in families:
                try:
                    rfam_family_id = family_name_rfam_id_mapping[rfam_family_name]
                except:
                    print 'Brak identyfikatora RFAM dla rodziny: ', rfam_family_name
                    continue
                infernal_repository.add_rfam_family_for_template(template_id, rfam_family_name, rfam_family_id, score)


if __name__ == "__main__":
    start_time = time.time()
    config = Config('config.ini')
    cmscan_path = config.get_infernal_cmscan()
    cmdatabase_path = config.get_infernal_cmdatabase()
    family_file_path = config.get_infernal_family_file()
    main_infernal_template_families(cmscan_path, cmdatabase_path, family_file_path)
    print("--- %s seconds ---" % (time.time() - start_time))
