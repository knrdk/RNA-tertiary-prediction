__author__ = 'Konrad Kopciuch'

from SCFG.ScoringMatrix import get_scoring_matrices
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from Repository.MongoTemplateRepository import MongoTemplateRepository
from Repository.MongoSCFGRepository import MongoSCFGRepository

def main_calculate_self_scfg_score(print_info=False):
    '''
    Funkcja dla szablonow zapisanych w bazie danych tworzy SCFG, nastepnie wylicza dopasowanie sekwencji szablonu
    do wlasnej SCFG i zapisuje ta wartosc w bazie danych. Dzieki temu przy obliczani wzglednego wyniku dopasowania do
    SCFG danego szablonu nie trzeba tej wartosci obliczac ponownie.
    :return: Funkcja nic nie zwraca
    '''
    single_matrix, double_matrix = get_scoring_matrices('./../config.ini')
    parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)

    template_repository = MongoTemplateRepository()
    scfg_repository = MongoSCFGRepository()

    for (template_id, template_sequence, template_secondary_structure) in template_repository.get_templates_info():
        scfg = parser.get_SCFG(template_secondary_structure, template_sequence)
        scfg.align(template_sequence)
        self_score = scfg.get_score()

        scfg_repository.add_scfg_self_score(template_id, self_score)
        if print_info:
            print template_id, self_score


if __name__ == '__main__':
    main_calculate_self_scfg_score(True)
