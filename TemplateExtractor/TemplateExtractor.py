# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB.Chain import Chain
import os

from moderna import load_model, clean_structure, examine_structure
import moderna.Template

from Utils.TemplateInfo import *
from Utils import Template


class TemplateExtractor:
    structure = None

    def __init__(self, file_path, logger=None):
        self.file_path = file_path
        self.structure_id = self.__get_structure_id().upper()
        self.logger = logger
        #self.logger.log_structure_id(self.structure_id)

    def __load_structure(self):
        if None == self.structure:
            parser = PDBParser()
            self.structure = parser.get_structure(self.structure_id, self.file_path)

    def __load_templates_info(self):
        parser = TemplateInfoParser(self.file_path)
        return parser.get_template_info()

    def get_templates(self):
        templates_info = dict(self.__load_templates_info())
        self.__load_structure()

        for chain in self.structure.get_chains():
            assert isinstance(chain, Chain)
            chain_id = chain.get_id()
            #self.logger.log_chain_id(chain_id)
            chain = load_model(data_type='chain', data=chain)
            clean_structure(chain)
            if self.__is_structure_valid(chain, chain_id):
                if self.__is_rna_structure(chain):
                    template_info = self.__get_template_info(chain_id, templates_info)
                    yield Template.Template(template_info, chain)
                else:
                    pass
                    #self.logger.log_not_rna_chain(chain_id)
            else:
                pass
                #self.logger.log_chain_not_valid(chain_id)

    def __is_rna_structure(self, structure): #structure must be cleaned before invoking this function
        assert isinstance(structure, moderna.RnaModel)
        return len(structure) > 1

    def __is_structure_valid(self, chain, chain_id):
        pdb_controller = examine_structure(chain, verbose=False)
        assert isinstance(pdb_controller, moderna.PdbController)

        if pdb_controller.has_problems():
            #self.logger.log_moderna_pdb_controller(pdb_controller)
            full_id = self.__get_full_id(chain_id)
            if not pdb_controller.continuous:
                pass
                #self.logger.log_chain_discontinuous(full_id)
            if pdb_controller.disconnected_residues:
                pass
                #self.logger.log_disconected_residues(full_id)
            #TODO: inne bledy: moderna/CheckPdb.py
            return False
        return True

    def __get_full_id(self, chain_id):
        return self.structure_id + "_" + chain_id

    def __get_structure_id(self):
        filename = os.path.basename(self.file_path)
        filename_without_extension = os.path.splitext(filename)[0]
        return filename_without_extension[3:]

    def __get_template_info(self, chain_id, templates_info):
        assert isinstance(templates_info, dict)
        if templates_info.has_key(chain_id):
            return templates_info[chain_id]
        else:
            return TemplateInfo(self.structure_id, chain_id)
