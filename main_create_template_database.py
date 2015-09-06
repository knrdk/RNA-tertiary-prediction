__author__ = 'rna'

from time import time

from Config import Config
from StructureDownloader.main_structure_downloader import main_structure_downloader
from TemplateExtractor.main_template_extractor import main_template_extractor
from TemplateExtractor.main_delete_redundant import main_delete_redundant


def main_create_template_database():
    config = Config('config.ini')
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    templates_directory = config.get_template_directory()

    print 'Pobieranie struktur z bazy PDB'
    main_structure_downloader(structures_directory, input_file_path)
    print 'Pobieranie zakonczone'

    print 'Wyodrebnianie szablonow z pobranych plikow PDB'
    main_template_extractor(structures_directory, templates_directory)
    print 'Wyodrebnie zakonczone'

    print 'Usuwanie powtarzajacych sie szablonow'
    main_delete_redundant(templates_directory)
    print 'Zakonczono usuwanie powtarzajacych sie szablonow'






if __name__ == '__main__':
    start_time = time()
    main_create_template_database()
    print("--- %s seconds ---" % (time() - start_time))