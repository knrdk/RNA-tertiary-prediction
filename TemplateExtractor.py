# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from Bio.PDB import PDBParser
from Bio.PDB.Chain import Chain
from moderna import load_model, clean_structure, write_model
import os


class TemplateExtractor:
    def __init__(self, template_path):
        self.template_path = template_path