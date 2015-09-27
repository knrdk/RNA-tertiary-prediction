__author__ = 'Konrad Kopciuch'

from SCFG.ScoringMatrix import get_scoring_matrices
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from Repository.MongoTemplateRepository import MongoTemplateRepository
from Repository.MongoSCFGRepository import MongoSCFGRepository
import Utils.ThreadPool as tp
from Config import Config
from main_infernal_template_families import main_infernal_template_families
from functools import partial


def process_template(config_file, tinfo):
    single_matrix, double_matrix = get_scoring_matrices(config_file)
    parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
    scfg_repository = MongoSCFGRepository()

    (template_id, template_sequence, template_secondary_structure) = tinfo
    scfg = parser.get_SCFG(template_secondary_structure, template_sequence)
    scfg.align(template_sequence)
    self_score = scfg.get_score()

    scfg_repository.add_scfg_self_score(template_id, self_score)
    #print template_id, self_score


def main_calculate_self_scfg_score(config_file):
    '''
    Funkcja dla szablonow zapisanych w bazie danych tworzy SCFG, nastepnie wylicza dopasowanie sekwencji szablonu
    do wlasnej SCFG i zapisuje ta wartosc w bazie danych. Dzieki temu przy obliczani wzglednego wyniku dopasowania do
    SCFG danego szablonu nie trzeba tej wartosci obliczac ponownie.
    :return: Funkcja nic nie zwraca
    '''
    template_repository = MongoTemplateRepository()

    func = partial(process_template, config_file)
    tinfos = list(template_repository.get_templates_info())
    pool = tp.get_thread_pool()
    pool.map(func, tinfos)


def preprocess_infernal(config_file):
    config = Config(config_file)
    cmscan_path = config.get_infernal_cmscan()
    cmdatabase_path = config.get_infernal_cmdatabase()
    family_file_path = config.get_infernal_family_file()
    main_infernal_template_families(cmscan_path, cmdatabase_path, family_file_path)


if __name__ == '__main__':
    main_calculate_self_scfg_score('config.ini')
    preprocess_infernal('config.ini')