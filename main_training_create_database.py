__author__ = 'Konrad Kopciuch'

from Config import Config
from main_training_structure_downloader import main_training_structure_downloader
from main_training_structure_extractor import main_template_extractor
from main_training_delete_redundant import main_delete_redundant


def main_training_create_database(config_file):
    config = Config(config_file)
    structures_directory = config.get_training_structures_directory()
    training_set_directory = config.get_training_set_directory()
    trainig_input_pdb_file = config.get_training_ndb_result_file()

    main_training_structure_downloader(structures_directory, trainig_input_pdb_file)
    main_template_extractor(structures_directory, training_set_directory)
    main_delete_redundant(training_set_directory)
