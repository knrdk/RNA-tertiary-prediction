__author__ = 'Konrad Kopciuch'

import os

import Utils.ThreadPool as tp
from functools import partial
from TemplateExtractor.TemplateExtractor import TemplateExtractor
from Utils.Template import TemplateWriter
from Utils import Template
from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Config import Config


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
            sequnce = template.get_sequence()
            if len(sequnce) < 250:
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
    pool = tp.get_thread_pool()
    result = pool.map(func, structures_path)
    print "Wyodrebniono szablonow: ", sum(result)



if __name__ == '__main__':
    config = Config('config.ini')
    structures_directory = '/home/rna/RNA/VerificationStructures'
    templates_directory = '/home/rna/RNA/VerificationSet'
    main_template_extractor(structures_directory, templates_directory)