# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
import os.path
import warnings

class TemplateInfo:
    def __init__(self, structure_id, chain_id, resolution, is_engineered):
        self.id = structure_id
        self.chain_id = chain_id
        self.resolution = resolution
        self.is_engineered = is_engineered

class TemplateInfoParser:
    def __init__(self, path):
        self.file_path = path
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
        self.__open_pdb_structure(parser, structure_id)
        header = parser.get_header()
        self.header = header

    def __open_pdb_structure(self, parser, structure_id):
        with warnings.catch_warnings(record=True) as w: #pdb parser raise warning when chain is doscontinuous
            parser.get_structure(structure_id, self.file_path)
            if(len(w)>0):
                for warn in w:
                    print warn #TODO: logowanie

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
