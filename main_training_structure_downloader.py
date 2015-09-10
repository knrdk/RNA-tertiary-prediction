__author__ = 'Konrad Kopciuch'

from multiprocessing import Pool, cpu_count
from functools import partial
from Config import Config
from StructureDownloader.NDBResultParser import NDBResultParser
from StructureDownloader.PDBStructureDownloader import PDBStructureDownloader
from Repository.MongoTemplateRepository import MongoTemplateRepository

def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)

def __download_structure(result_directory, pdb_id):
    try:
        PDBStructureDownloader.download_and_write(pdb_id, result_directory)
        return True
    except: return False

def main_training_structure_downloader(result_directory, input_file_path):
    template_repository = MongoTemplateRepository()
    structure_as_templates = template_repository.get_structures_id()
    pdb_ids = []
    for pdb_id in NDBResultParser.get_pdb_ids(input_file_path):
        if not pdb_id in structure_as_templates:
            pdb_ids.append(pdb_id)

    func = partial(__download_structure, result_directory)
    pool = __get_thread_pool()
    results = pool.map(func, pdb_ids)

    downloaded_structure, failed_structures = 0, 0
    for (index, value) in enumerate(results):
        if value:
            downloaded_structure += 1
        else:
            pdb_id = pdb_ids[index]
            print 'Blad przy sciaganiu pliku: ', pdb_id

    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


if __name__ == '__main__':
    config = Config('config.ini')
    structures_directory = config.get_training_structures_directory()
    input_file_path = config.get_training_ndb_result_file()
    main_training_structure_downloader(structures_directory, input_file_path)