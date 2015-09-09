__author__ = 'Konrad Kopciuch'

import os

from Utils.Template import *
from TemplateExtractor.TemplateExtractor import TemplateExtractor
from TemplateExtractor.TemplateExtractorLogger import TemplateExtractorLogger
from Utils import Template
from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Config import Config


def main_template_extractor(structures_directory, templates_directory):
    logger = TemplateExtractorLogger()
    writer = TemplateWriter(templates_directory)
    repo = MongoTrainingTemplateRepository()
    for file_path in os.listdir(structures_directory):
        if file_path.endswith(".ent") or file_path.endswith(".pdb"):
            print 'Wyodrebnianie szablonow z pliku: ', file_path
            structure_path = structures_directory + file_path
            te = TemplateExtractor(structure_path, logger)
            templates = te.get_templates()
            for template in templates:
                assert isinstance(template, Template.Template)
                id = repo.add_template(template)
                tinfo = template.template_info
                writer.write(template)
                print tinfo.id, tinfo.chain_id


if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_training_structures_directory()
    templates_directory = config.get_training_set_directory()
    main_template_extractor(structures_directory, templates_directory)