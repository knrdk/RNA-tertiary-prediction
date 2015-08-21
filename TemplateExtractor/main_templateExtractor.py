__author__ = 'Konrad Kopciuch'

from Template import *
from TemplateExtractor import TemplateExtractor
import Template
import os
from TemplateExtractorLogger import TemplateExtractorLogger
from TemplateRepository import MongoTemplateRepository

structures_directory = "C:\\RNA-structures\\"
templates_directory = "C:\\RNA-templates\\"

def main():
    logger = TemplateExtractorLogger()
    logger.log_start(structures_directory, templates_directory)
    writer = TemplateWriter(templates_directory)
    repo = MongoTemplateRepository.MongoTemplateRepository()
    for file in os.listdir(structures_directory):
        if file.endswith(".ent") or file.endswith(".pdb"):
            logger.log_filename(file)
            structure_path = structures_directory + file
            logger.log_structure_path(structure_path)
            te = TemplateExtractor(structure_path, logger)
            templates = te.get_templates()
            for template in templates:
                assert isinstance(template, Template.Template)
                id = repo.add_template(template)
                tinfo = template.template_info
                writer.write(template)
                logger.log_template_extracted(id, tinfo)


if __name__ == '__main__':
    main()