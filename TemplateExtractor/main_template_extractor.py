__author__ = 'Konrad Kopciuch'

import os

from Utils.Template import *
from TemplateExtractor import TemplateExtractor
from Utils import Template
from TemplateExtractorLogger import TemplateExtractorLogger
from Repository import MongoTemplateRepository
from Config import Config
import multiprocessing

def process_structure_file(file_path, repo, writer, logger):
    if file_path.endswith(".ent") or file_path.endswith(".pdb"):
            print 'Wyodrebnianie szablonow z pliku: ', file_path
            logger.log_filename(file_path)
            structure_path = structures_directory + file_path
            logger.log_structure_path(structure_path)
            te = TemplateExtractor(structure_path, logger)
            templates = te.get_templates()
            for template in templates:
                assert isinstance(template, Template.Template)
                id = repo.add_template(template)
                tinfo = template.template_info
                writer.write(template)
                logger.log_template_extracted(id, tinfo)
                print tinfo.id, tinfo.chain_id

def main_template_extractor(structures_directory, templates_directory):
    logger = TemplateExtractorLogger()
    logger.log_start(structures_directory, templates_directory)
    writer = TemplateWriter(templates_directory)
    repo = MongoTemplateRepository.MongoTemplateRepository()
    structures_path = list()
    for file_path in os.listdir(structures_directory):
        structures_path.append((file_path, repo, writer, logger))

    try:
        cpus = multiprocessing.cpu_count()
    except NotImplementedError:
        cpus = 2   # arbitrary default

    pool = multiprocessing.Pool(processes=cpus)
    pool.map(process_structure_file, structures_path)



if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_structure_directory()
    templates_directory = config.get_template_directory()
    main_template_extractor(structures_directory, templates_directory)