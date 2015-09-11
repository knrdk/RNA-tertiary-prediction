__author__ = 'Konrad Kopciuch'

import logging
import datetime
import sys
from multiprocessing import Pool, cpu_count
from functools import partial
from Config import Config
import Utils.ThreadPool as tp
from StructureDownloader.NDBResultParser import NDBResultParser
from StructureDownloader.PDBStructureDownloader import PDBStructureDownloader


def __get_logger():
    logger = logging.getLogger()
    fh = logging.FileHandler('log_template_download_structure.txt')
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def __download_structure(result_directory, pdb_id):
    try:
        PDBStructureDownloader.download_and_write(pdb_id, result_directory)
        return True
    except: return False


def main_template_download_structure(result_directory, input_file_path):
    logger = __get_logger()
    logger.info("Downloading started: %s", datetime.datetime.now())

    pdb_ids = list(NDBResultParser.get_pdb_ids(input_file_path))
    func = partial(__download_structure, result_directory)
    pool = tp.get_thread_pool()
    results = pool.map(func, pdb_ids)

    downloaded_structure, failed_structures = 0, 0
    for (index, value) in enumerate(results):
        if value:
            downloaded_structure += 1
        else:
            id = pdb_ids[index]
            print 'Blad przy sciaganiu pliku: ', id
            logger.error("ERROR while downloading: %s", id)

    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


def __get_data_from_config():
    config = Config('config.ini')
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    return structures_directory, input_file_path


if __name__ == '__main__':
    if len(sys.argv) == 3:
        structures_directory, input_file_path = sys.argv[1], sys.argv[2]
    else: #wczytaj z pliku konfiguracyjnego
        structures_directory, input_file_path = __get_data_from_config()
    main_template_download_structure(structures_directory, input_file_path)