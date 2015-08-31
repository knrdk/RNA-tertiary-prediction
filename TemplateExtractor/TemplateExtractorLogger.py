__author__ = 'Konrad Kopciuch'

import logging
from datetime import datetime

from TemplateInfo import TemplateInfo

log_file = "template_extractor_log.txt"

class TemplateExtractorLogger(object):
    def __init__(self):
        self.logger = logger = logging.getLogger()
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)
        logger.setLevel(logging.WARNING)

    def log_start(self, structures_directory, templates_directory):
        self.logger.info("TemplateExtractor started: %s", datetime.now())
        self.logger.info("Structures directory: %s", structures_directory)
        self.logger.info("Templates directory: %s", templates_directory)

    def log_filename(self, filename):
        self.logger.debug("File found: %s", filename)

    def log_structure_path(self, path):
        self.logger.debug("Structure file path: %s", path)

    def log_template_extracted(self, id, tinfo):
        assert isinstance(tinfo, TemplateInfo)
        self.logger.debug("Template added to database id: %s, structure_id: %s, chain_id: %s"
                         ,id
                         , tinfo.id
                         , tinfo.chain_id)

    def log_structure_id(self, id):
        self.logger.debug("Structure in file: %s", id)

    def log_chain_id(self, id):
        self.logger.debug("Chain id: %s", id)

    def log_chain_not_valid(self, id):
        self.logger.warning("Chain is not valid: %s", id)

    def log_not_rna_chain(self, id):
        self.logger.debug("Not RNA chain: %s", id)

    def log_moderna_pdb_controller(self, pc):
        self.logger.debug(pc)

    def log_chain_discontinuous(self, id):
        self.logger.warning("Chain is discontinuous")

    def log_disconected_residues(self, id):
        self.logger.warning("Some residues are disconnected")