__author__ = 'rna'

from ConfigParser import ConfigParser

class Config:
    config_file_path = './../config.ini'

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(self.config_file_path)

    def get_structure_directory(self):
        section = 'Template'
        option = 'structure_directory'
        return self.config.get(section, option)

    def get_template_directory(self):
        section = 'Template'
        option = 'template_directory'
        return self.config.get(section, option)