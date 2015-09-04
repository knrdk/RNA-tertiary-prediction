__author__ = 'rna'

from ConfigParser import ConfigParser


class Config:

    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_structure_directory(self):
        section = 'Template'
        option = 'structure_directory'
        return self.config.get(section, option)

    def get_template_directory(self):
        section = 'Template'
        option = 'template_directory'
        return self.config.get(section, option)

    def get_ndb_result_file_path(self):
        section = 'Template'
        option = 'ndb_result_file'
        return self.config.get(section, option)