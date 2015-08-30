__author__ = 'Konrad Kopciuch'
import logging
import sys
from datetime import datetime

from NDBResultParser import NDBResultParser
from PDBStructureDownloader import PDBStructureDownloader


def __get_logger():
    logger = logging.getLogger()
    fh = logging.FileHandler('log.txt')
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger

def main(result_directory, input_file_path):
    loggger = __get_logger()
    loggger.info("Downloading started: %s", datetime.now())

    all_structures, failed_structures = 0, 0
    for id in NDBResultParser.get_pdb_ids(input_file_path):
        all_structures+=1
        try:
            PDBStructureDownloader.download_and_write(id, result_directory)
        except:
            failed_structures+=1
            loggger.error("ERROR %s", str(id))
    downloaded_structure = all_structures - failed_structures
    print 'liczba sciagnietych plikow pdb: ', downloaded_structure
    print 'liczba plikow przy pobieraniu ktorych wystapily bledy: ', failed_structures


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "main_structure_downloader.py result_directory input_file_path"
    result_directory = sys.argv[1]
    input_file_path = sys.argv[2]
    main(result_directory, input_file_path)