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

    def get_ribosum_matrix_path(self):
        section = 'SCFG'
        option = 'ribosum_matrix'
        return self.config.get(section, option)

    def get_training_results_path(self):
        section = 'Training'
        option = 'training_results_file_path'
        return self.config.get(section, option)

    def get_training_set_directory(self):
        section = 'Training'
        option = 'training_set_directory'
        return self.config.get(section, option)

    def get_training_structures_directory(self):
        section = 'Training'
        option = 'training_structures_directory'
        return self.config.get(section, option)

    def get_training_ndb_result_file(self):
        section = 'Training'
        option = 'ndb_result_file'
        return self.config.get(section, option)