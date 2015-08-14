# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
from Bio.PDB.Chain import Chain
from moderna import load_model, clean_structure
import moderna.Template
from TemplateInfo import *
import Template
import os


class TemplateExtractor:
    structure = None

    def __init__(self, file_path):
        self.file_path = file_path

    def __load_structure(self):
        if None == self.structure:
            parser = PDBParser()
            self.structure = parser.get_structure(self.__get_structure_id(), self.file_path)

    def __load_templates_info(self):
        parser = TemplateInfoParser(self.file_path)
        return parser.get_template_info()

    def get_templates(self):
        templates_info = dict(self.__load_templates_info())
        self.__load_structure()

        for chain in self.structure.get_chains():
            assert isinstance(chain, Chain)
            chain_id = chain.get_id()
            template = load_model(data_type='chain', data = chain)
            clean_structure(template)
            if self.__is_rna_structure(template):
                yield Template.Template(templates_info[chain_id], template)

    def __is_rna_structure(self, structure): #structure must be cleaned before invoking this function
        assert isinstance(structure, moderna.RnaModel)
        return len(structure)

    def __get_structure_id(self):
        filename = os.path.basename(self.file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        return filename_without_extension