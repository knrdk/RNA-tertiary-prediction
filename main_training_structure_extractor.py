__author__ = 'Konrad Kopciuch'

import os

from multiprocessing import Pool, cpu_count
from functools import partial
from TemplateExtractor.TemplateExtractor import TemplateExtractor
from Utils.Template import TemplateWriter
from Utils import Template
from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Config import Config


def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)

def process_structure_file(structures_directory, templates_directory, file_path):
    i = 0
    if file_path.endswith(".ent") or file_path.endswith(".pdb"):
        writer = TemplateWriter(templates_directory)
        repo = MongoTrainingTemplateRepository()

        print 'Wyodrebnianie szablonow z pliku: ', file_path
        structure_path = structures_directory + file_path
        te = TemplateExtractor(structure_path)
        templates = te.get_templates()
        for template in templates:
            i += 1
            assert isinstance(template, Template.Template)
            id = repo.add_template(template)
            tinfo = template.template_info
            writer.write(template)
            print "Wyodrebniono lancuch: ", tinfo.id, tinfo.chain_id
    return i

def main_template_extractor(structures_directory, templates_directory):

    func = partial(process_structure_file, structures_directory, templates_directory)

    structures_path = list(os.listdir(structures_directory))
    print "Znaleziono plikow pdb:" ,len(structures_path)
    pool = __get_thread_pool()
    result = pool.map(func, structures_path)
    print "Wyodrebniono szablonow: ", sum(result)



if __name__ == '__main__':
    config = Config('config.ini')
    structures_directory = config.get_training_structures_directory()
    templates_directory = config.get_training_set_directory()
    main_template_extractor(structures_directory, templates_directory)