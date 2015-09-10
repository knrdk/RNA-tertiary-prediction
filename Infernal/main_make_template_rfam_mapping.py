__author__ = 'Konrad Kopciuch'

from ConfigParser import ConfigParser
import time

from Repository.MongoTemplateRepository import MongoTemplateRepository
from Repository.MongoInfernalRepository import MongoInfernalRepository
from Infernal import Infernal
from FamilyFileParser import FamilyFileParser


def get_config(path):
    config = ConfigParser()
    config.read(path)
    section = 'Infernal'
    options = config.options(section)
    dict1 = dict()
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            dict1[option] = None
    return dict1

def __get_infernal():
    config = get_config("config.ini")
    return Infernal(config)

def __get_family_name_rfam_id_mapping():
    path = '/home/rna/RNA/family.txt'
    parser = FamilyFileParser(path)
    mapping = parser.get_family_name_rfam_id_mapping()
    return mapping

def main_make_template_rfam_mapping():
    family_name_rfam_id_mapping = __get_family_name_rfam_id_mapping()
    infernal = __get_infernal()
    template_repository = MongoTemplateRepository()
    infernal_repository = MongoInfernalRepository()

    for (template_id, sequence, resolution) in template_repository.get_all_unmodified_sequences():
        families = infernal.get_families_for_sequence(sequence)
        if len(families) > 0:
            for (family_name, score) in families:
                try:
                    rfam_family_id = family_name_rfam_id_mapping[family_name]
                except:
                    print 'Brak identyfikatora RFAM dla rodziny: ', family_name
                    continue
                infernal_repository.add_rfam_family_for_template(template_id, rfam_family_id, score)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
