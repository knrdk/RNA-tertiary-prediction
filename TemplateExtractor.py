# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
from Bio.PDB.Chain import Chain
from Bio.PDB.Structure import Structure
from moderna import load_model, clean_structure
import os

class TemplateExtractor:
    def __init__(self, template_path):
        self.template_path = template_path
        (self.PDB_header, self.PDB_structure) = self.__read_PDB(template_path)

    def __read_PDB(self, pdb_path):
        structure_name = self.__get_structure_name(pdb_path)
        self.__get_structure_name(pdb_path)
        parser = PDBParser(get_header=True)
        structure = parser.get_structure(structure_name, pdb_path)
        header = parser.get_header()
        resolution = self.__get_resolution(header) #TODO: przyda się później
        return (header, structure)

    def __get_structure_name(self, pdb_path):
        filename = os.path.basename(pdb_path)
        filename_without_extension = os.path.splitext(filename)[0]
        return filename_without_extension

    def get_unique_chains_ids(self):
        ids = set([])
        compounds = self.PDB_header['compound']
        for i in compounds:
            chain_info = compounds[i]
            is_RNA_chain = self.__is_RNA_chain(chain_info)
            if is_RNA_chain:
                chain_id = self.__get_chain_id(chain_info)
                is_engineered = self.__is_engineered(chain_info) #TODO: czy takie też uwzględniać ?
                ids.add(chain_id)
        return ids

    def __get_cleaned_sequence(self, chain):
        assert isinstance(chain, Chain)
        moderna_chain = load_model(chain,chain.get_id(),'chain')
        clean_structure(moderna_chain)
        return moderna_chain.get_sequence()

    def __get_resolution(self, header):
        return float(header['resolution'])

    def __is_RNA_chain(self,chain_info):
        molecule_info = chain_info['molecule']
        molecule_type = molecule_info.split()[0].upper()
        if molecule_type == "RNA":
            return True
        elif molecule_type =="PROTEIN":
            return False
        else:
            #TODO: warning
            return False

    def __is_engineered(self,chain_info):
        return chain_info['engineered']=='yes'

    def __get_chain_id(self, chain_info):
        return chain_info['chain'].upper()
