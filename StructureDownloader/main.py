__author__ = 'Konrad Kopciuch'
from NDBResultParser import NDBResultParser
from PDBStructureDownloader import PDBStructureDownloader

if __name__ == '__main__':
    result_directory = "C:\\RNA-structures"
    result_file_path = result_directory + "\\Result.xls"
    structure_ids = NDBResultParser.get_pdb_ids(result_file_path)

    for id in structure_ids:
        try:
            PDBStructureDownloader.download_and_write(id, result_directory)
        except:
            #TODO: logowanie
            print 'blad' + str(id)