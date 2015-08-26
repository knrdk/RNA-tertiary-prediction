__author__ = 'Konrad Kopciuch'
from NDBResultParser import NDBResultParser
from PDBStructureDownloader import PDBStructureDownloader

def main():
    result_directory = "C:\\RNA-structures"
    result_file_path = result_directory + "\\Result.xls"

    structure_ids = NDBResultParser.get_pdb_ids(result_file_path)

    all_structures = 0
    failed_structures = 0
    for id in structure_ids:
        all_structures+=1
        try:
            PDBStructureDownloader.download_and_write(id, result_directory)
        except:
            failed_structures+=1
            #TODO: logowanie
            print 'blad' + str(id)
    print all_structures, failed_structures


if __name__ == '__main__':
    main()