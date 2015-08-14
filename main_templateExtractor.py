__author__ = 'Konrad Kopciuch'

from TemplateInfo import *
from Template import *
from TemplateExtractor import TemplateExtractor
import Template
from moderna import remove_all_modifications
structure_directory = "C:\\RNA-structures\\"
template_directory = "C:\\RNA-templates\\"

writer = TemplateWriter(template_directory)

import os
from TemplateRepository import MongoTemplateRepository

repo = MongoTemplateRepository.MongoTemplateRepository()

for file in os.listdir(structure_directory):
    if file.endswith(".ent"):
        structure_path = structure_directory + file
        te = TemplateExtractor(structure_path)
        templates = te.get_templates()
        for template in templates:
            assert isinstance(template, Template.Template)
            print repo.add_template(template)
            '''tinfo = template.template_info
            assert isinstance(tinfo, TemplateInfo)
            print tinfo.get_id()
            print tinfo.chain_id
            print tinfo.resolution
            print tinfo.is_engineered
            print(template.get_sequence())
            #print(template.get_secondary_structure())a
            remove_all_modifications(template.structure)
            print template.get_sequence()
            '''
            writer.write(template)
            print("---")