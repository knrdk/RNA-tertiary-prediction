# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
import os.path
import warnings

class TemplateInfo:
    def __init__(self, structure_id, chain_id, resolution, is_engineered):
        self.__set_id(structure_id)
        self.chain_id = chain_id
        self.resolution = resolution
        self.is_engineered = is_engineered

    def __set_id(self, structure_id):
        assert isinstance(structure_id, str)
        self.id = structure_id.upper()

    def get_id(self):
        return self.id



class TemplateInfoParser:
    known_other_molecule_types = {'PROTEIN', 'DNA'}
    def __init__(self, path):
        self.file_path = path
        self.structure_id = self.__get_structure_id()
        self.header = None

    def get_template_info(self):
        if None == self.header:
            self.__read_pdb_header()
        return self.__get_template_info_impl()

    def __get_template_info_impl(self):
        compounds = self.header['compound']
        resolution = self.__get_resolution()
        for i in compounds:
            chain_info = compounds[i]
            chains_id = self.__get_chains_id(chain_info)
            for chain_id in chains_id:
                is_engineered = self.__is_engineered(chain_info)
                templ_info = TemplateInfo(self.structure_id, chain_id, resolution, is_engineered)
                yield chain_id, templ_info

    def __get_structure_id(self):
        filename = os.path.basename(self.file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        return filename_without_extension[3:] #deleting "pdb" from begining

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
                    print "WARN" + warn #TODO: logowanie

    def __get_resolution(self):
        try:
            return float(self.header['resolution'])
        except: return -1

    def __is_engineered(self,chain_info):
        try:
            return chain_info['engineered']=='yes'
        except:
            return None

    def __get_chains_id(self, chain_info):
        ids = chain_info['chain'].upper().split(",")
        return map(str.strip, ids)
