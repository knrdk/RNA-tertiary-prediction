__author__ = 'Konrad Kopciuch'

import logging
import datetime
from multiprocessing import Pool, cpu_count
from functools import partial
from Config import Config
from StructureDownloader.NDBResultParser import NDBResultParser
from StructureDownloader.PDBStructureDownloader import PDBStructureDownloader


def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)

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


def main_template_download_structure(result_directory, input_file_path):
    logger = __get_logger()
    logger.info("Downloading started: %s", datetime.datetime.now())

    all_structures, failed_structures = 0, 0
    pdb_ids = list(NDBResultParser.get_pdb_ids(input_file_path))

    func = partial(__download_structure, result_directory)
    pool = __get_thread_pool()
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


if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    main_template_download_structure(structures_directory, input_file_path)