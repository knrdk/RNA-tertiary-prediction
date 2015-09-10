__author__ = 'Konrad Kopciuch'

import logging
from datetime import datetime

from Config import Config
from StructureDownloader.NDBResultParser import NDBResultParser
from StructureDownloader.PDBStructureDownloader import PDBStructureDownloader


def __get_logger():
    logger = logging.getLogger()
    fh = logging.FileHandler('structure_downloader_log.txt')
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def __download_structure(result_directory, pdb_id):
    try:
        PDBStructureDownloader.download_and_write(pdb_id, result_directory)
        return True
    except: return False


def main_structure_downloader(result_directory, input_file_path):
    logger = __get_logger()
    logger.info("Downloading started: %s", datetime.now())

    all_structures, failed_structures = 0, 0
    for pdb_id in NDBResultParser.get_pdb_ids(input_file_path):
        all_structures += 1
        result = __download_structure(result_directory, pdb_id)
        if not result:
            failed_structures += 1
            logger.error("ERROR while downloading structure from PDB, id: %s", pdb_id)

    downloaded_structure = all_structures - failed_structures
    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    main_structure_downloader(structures_directory, input_file_path)