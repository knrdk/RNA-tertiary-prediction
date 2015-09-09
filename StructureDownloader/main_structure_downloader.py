__author__ = 'Konrad Kopciuch'
import logging
from datetime import datetime

from Config import Config
from NDBResultParser import NDBResultParser
from PDBStructureDownloader import PDBStructureDownloader
from multiprocessing import Pool, cpu_count
from functools import partial


def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)


def __get_logger():
    logger = logging.getLogger()
    fh = logging.FileHandler('log.txt')
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger

def download_pdb_file(result_directory, pdb_id):
    try:
        PDBStructureDownloader.download_and_write(pdb_id, result_directory)
        return True
    except:
        return False

def main_structure_downloader(result_directory, input_file_path):
    loggger = __get_logger()
    loggger.info("Sciaganie rozpoczete: %s", datetime.now())

    func = partial(download_pdb_file, result_directory)
    ids = list(NDBResultParser.get_pdb_ids(input_file_path))
    pool = __get_thread_pool()

    result = pool.map(func, ids)

    downloaded_structure, failed_structures = 0, 0
    for x in result:
        if x:
            downloaded_structure += 1
        else:
            failed_structures += 1


    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_structure_directory()
    input_file_path = config.get_ndb_result_file_path()
    main_structure_downloader(structures_directory, input_file_path)