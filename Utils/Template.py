# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from moderna import write_model
from moderna import ModernaSequence
from TemplateInfo import TemplateInfo

class Template:
    def __init__(self, template_info, structure):
        self.template_info = template_info
        self.structure = structure

    def get_sequence(self):
        seq = self.structure.get_sequence()
        assert isinstance(seq, ModernaSequence.Sequence)
        return str(seq).upper()

    def get_sequence_without_modifications(self):
        seq = self.structure.get_sequence()
        assert isinstance(seq, ModernaSequence.Sequence)
        return str(seq.seq_without_modifications).upper()

    def get_secondary_structure(self):
        return self.structure.get_secstruc()



class TemplateWriter:
    def __init__(self, directory):
        self.directory = directory #usuwanie/dodawanie "//" z końca

    def write(self, template):
        assert isinstance(template, Template)
        template_info = template.template_info
        assert isinstance(template_info, TemplateInfo)
        filename = template_info.id + "_" + template_info.chain_id + ".pdb"
        path = self.directory + filename
        write_model(template.structure, path)

