__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser

class TemplateExtractor:

    def __int__(self, template_path):
        self.template_path = template_path
