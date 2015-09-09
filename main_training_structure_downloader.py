__author__ = 'Konrad Kopciuch'

from Config import Config
from StructureDownloader.NDBResultParser import NDBResultParser
from StructureDownloader.PDBStructureDownloader import PDBStructureDownloader

def main_structure_downloader(result_directory, input_file_path):
    all_structures, failed_structures = 0, 0
    for id in NDBResultParser.get_pdb_ids(input_file_path):
        all_structures+=1
        try:
            PDBStructureDownloader.download_and_write(id, result_directory)
        except:
            failed_structures+=1
    downloaded_structure = all_structures - failed_structures
    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


if __name__ == '__main__':
    config = Config('./config.ini')
    structures_directory = config.get_training_structures_directory()
    input_file_path = config.get_training_ndb_result_file()
    main_structure_downloader(structures_directory, input_file_path)