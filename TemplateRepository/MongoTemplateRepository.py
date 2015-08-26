from re import template

__author__ = 'Konrad Kopciuch'

import Template
from pymongo import MongoClient
from moderna import ModernaSequence

class MongoTemplateRepository():
    def __init__(self):
        client = MongoClient()
        self.db = client.RNA

    def add_template(self, template):
        assert isinstance(template, Template.Template)
        tinfo = template.template_info
        assert isinstance(tinfo, Template.TemplateInfo)
        data =  {
                "structure_id" : tinfo.id,
                "chain_id" : tinfo.chain_id,
                "sequence" : template.get_sequence(),
                "sequence_without_modifications" : template.get_sequence_without_modifications(),
                "secondary_structure" : template.get_secondary_structure()
                }
        table = self.__get_templates_table()
        id = table.insert_one(data).inserted_id
        return id

    def __get_templates_table(self):
        return self.db.templates
