__author__ = 'Konrad Kopciuch'

from time import time

from Config import Config
from main_structure_downloader import main_structure_downloader
from TemplateExtractor.main_template_extractor import main_template_extractor
from TemplateExtractor.main_delete_redundant import main_delete_redundant
from TemplateExtractor.main_calculate_self_scfg_score import main_calculate_self_scfg_score


def main_create_template_database(config_file):
    config = Config(config_file)
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    templates_directory = config.get_template_directory()

    start_time = time()

    print 'Pobieranie struktur z bazy PDB'
    start_time_part = time()
    main_structure_downloader(structures_directory, input_file_path)
    print("--- %s seconds ---" % (time() - start_time_part))
    print 'Pobieranie zakonczone'

    print 'Wyodrebnianie szablonow z pobranych plikow PDB'
    start_time_part = time()
    main_template_extractor(structures_directory, templates_directory)
    print("--- %s seconds ---" % (time() - start_time_part))
    print 'Wyodrebnie zakonczone'

    print 'Usuwanie powtarzajacych sie szablonow'
    start_time_part = time()
    main_delete_redundant(templates_directory)
    print("--- %s seconds ---" % (time() - start_time_part))
    print 'Zakonczono usuwanie powtarzajacych sie szablonow'

    print 'Zapisywanie informacji o wlasnych wynikach SCFG'
    start_time_part = time()
    main_calculate_self_scfg_score('config.ini')
    print("--- %s seconds ---" % (time() - start_time_part))
    print 'Zakonczono zapisywanie informacji o wynikach SCFG'

    print 'Zakonczono tworzenie bazy szablonow'
    print("--- %s seconds ---" % (time() - start_time))


if __name__ == '__main__':
    main_create_template_database('config.ini')
