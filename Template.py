# coding=UTF-8
__author__ = 'Konrad Kopciuch'

from moderna import load_template, write_model, clean_structure
from TemplateInfo import TemplateInfo

class Template:
    def __init__(self, template_info, structure):
        self.template_info = template_info
        self.structure = structure

    def get_sequence(self):
        return self.structure.get_sequence()

    def get_secondary_structure(self):
        return self.structure.get_secstruc()


class TemplateParser:
    def __init__(self, template_info, path):
        self.template_info = template_info
        self.path = path

    def get_template(self):
        tmpl_info = self.template_info
        assert isinstance(tmpl_info, TemplateInfo)
        tmpl = load_template(self.path, tmpl_info.chain_id)
        TemplateParser.__preprocess_template(tmpl)
        return Template(tmpl_info, tmpl)

    @staticmethod
    def __preprocess_template(template):
        clean_structure(template)

class TemplateWriter:

    @staticmethod
    def write(template, path):
        assert isinstance(template, Template)
        write_model(template.structure, path)

