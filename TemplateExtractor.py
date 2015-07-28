# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
from Bio.PDB.Chain import Chain
from moderna import load_model, clean_structure, write_model
import os


class TemplateExtractor:
    def __init__(self, template_path):
        self.template_path = template_path
        (self.PDB_header, self.PDB_structure) = self.__read_PDB(template_path)
        self.unique_chains = None

    def __read_PDB(self, pdb_path):
        parser = PDBParser(get_header=True)
        structure = parser.get_structure("str_id", pdb_path)
        return structure


class TemplateInfo:
    def __init__(self, structure_id, chain_id, resolution, is_engineered):
        self.id = structure_id
        self.chain_id = chain_id
        self.resolution = resolution
        self.is_engineered = is_engineered

class TemplateInfoParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.structure_id = self.__get_structure_id()
        self.header = None

    def get_template_info(self):
        if None == self.header:
            self.__read_pdb_header()
        return self.__get_template_info_impl()

    def __get_template_info_impl(self):
        unique_chains = []
        compounds = self.header['compound']
        resolution = self.__get_resolution()
        for i in compounds:
            chain_info = compounds[i]
            is_RNA_chain = self.__is_rna_chain(chain_info)
            if is_RNA_chain:
                chain_id = self.__get_chain_id(chain_info)
                is_engineered = self.__is_engineered(chain_info)
                templ_info = TemplateInfo(self.structure_id, chain_id, resolution, is_engineered)
                unique_chains.append(templ_info)
        return unique_chains

    def __get_structure_id(self):
        filename = os.path.basename(self.file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        return filename_without_extension

    def __read_pdb_header(self):
        structure_id = self.__get_structure_id()
        parser = PDBParser(get_header=True)
        parser.get_structure(structure_id, self.file_path)
        header = parser.get_header()
        self.header = header

    def __get_resolution(self):
        return float(self.header['resolution'])

    def __is_rna_chain(self, chain_info):
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


class Template:
    def __init__(self, template_info, structure):
        self.template_info = template_info
        self.structure = structure

    def get_sequence(self):
        self.__initialize_moderna_chain()
        return self.moderna_chain.get_sequence()

    def get_secondary_structure(self):
        self.__initialize_moderna_chain()
        return self.moderna_chain.get_secstruc()

    def __initialize_moderna_chain(self):
        if None == self.moderna_chain:
            self.__initialize_moderna_chain()

    def __initialize_moderna_chain_impl(self):
        chain = self.chain
        assert isinstance(chain, Chain)
        self.moderna_chain = load_model(chain, chain.get_id(), 'chain')
        self.__clean_moderna_chain()

    def __clean_moderna_chain(self):
        if None != self.moderna_chain:
            clean_structure(self.moderna_chain)

class TemplateWriter:
    structure_chain_separator = "_"
    extension = ".pdb"

    def __init__(self, template):
        self.template = template

    def write(self, directory):
        path = self.__get_path(directory)
        write_model(self.template.moderna_chain, path)

    def __get_path(self, directory):
        filename = self.template.structure_id + self.structure_chain_separator + self.template.chain + self.extension
        path = os.path.join(directory,filename)
        print path
