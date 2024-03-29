__author__ = 'Konrad Kopciuch'

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

    def get_feature_vectors_path(self):
        section = 'Training'
        option = 'feature_vectors_file_path'
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

    def get_svm_file(self):
        section = 'SVM'
        option = 'svm_file'
        return self.config.get(section, option)

    def get_infernal_cmscan(self):
        section = 'Infernal'
        option = 'cmscan'
        return self.config.get(section, option)

    def get_infernal_cmdatabase(self):
        section = 'Infernal'
        option = 'cmdatabase'
        return self.config.get(section, option)

    def get_infernal_family_file(self):
        section = 'Infernal'
        option = 'familyfile'
        return self.config.get(section, option)