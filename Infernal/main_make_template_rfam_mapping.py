__author__ = 'Konrad Kopciuch'

from ConfigParser import ConfigParser
from Repository.MongoTemplateRepository import MongoTemplateRepository
from Infernal import Infernal
from FamilyFileParser import FamilyFileParser

import time

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

def main():
    family_name_rfam_id_mapping = __get_family_name_rfam_id_mapping()
    infernal = __get_infernal()
    repo = MongoTemplateRepository()

    for (id, sequence) in repo.get_all_unmodified_sequences():
        families = infernal.get_families_for_sequence(sequence)
        if len(families) > 0:
            print id
            print sequence
            for (family_name, score) in families:
                print family_name_rfam_id_mapping[family_name]
                print family_name
                print score
            print "---"

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
