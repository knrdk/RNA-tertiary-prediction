__author__ = 'Konrad Kopciuch'
from Bio.PDB import PDBList

class PDBStructureDownloader:

    @staticmethod
    def download_and_write(pdb_id, directory):
        pdb_list = PDBList()
        pdb_list.retrieve_pdb_file(pdb_id,pdir=directory)
        return True

