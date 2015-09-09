__author__ = 'Konrad Kopciuch'

import os

from Utils.Template import *
from TemplateExtractor import TemplateExtractor
from Utils import Template
from TemplateExtractorLogger import TemplateExtractorLogger
from Repository import MongoTemplateRepository
from Config import Config
from multiprocessing import Pool, cpu_count
from functools import partial

def process_structure_file(templates_directory, file_path):
    print templates_directory
    return
    if file_path.endswith(".ent") or file_path.endswith(".pdb"):
            repo = MongoTemplateRepository()
            writer = TemplateWriter(templates_directory)
            print 'Wyodrebnianie szablonow z pliku: ', file_path
            #logger.log_filename(file_path)
            structure_path = structures_directory + file_path
            #logger.log_structure_path(structure_path)
            te = TemplateExtractor(structure_path)
            templates = te.get_templates()
            for template in templates:
                assert isinstance(template, Template.Template)
                id = repo.add_template(template)
                tinfo = template.template_info
                writer.write(template)
                #logger.log_template_extracted(id, tinfo)
                print tinfo.id, tinfo.chain_id

def main_template_extractor(structures_directory, templates_directory):
    logger = TemplateExtractorLogger()
    logger.log_start(structures_directory, templates_directory)
    structures_path = list(os.listdir(structures_directory))

    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 2   # arbitrary default

    func = partial(process_structure_file, templates_directory)

    pool = Pool(processes=cpus)
    pool.map(func, structures_path)



if __name__ == '__main__':
    config = Config('./../config.ini')
    structures_directory = config.get_structure_directory()
    templates_directory = config.get_template_directory()
    main_template_extractor(structures_directory, templates_directory)