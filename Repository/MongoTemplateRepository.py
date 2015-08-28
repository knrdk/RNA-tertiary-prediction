__author__ = 'Konrad Kopciuch'

import Template
from pymongo import MongoClient

field_structure_id = "structure_id"
field_chain_id = "chain_id"
field_sequence = "sequence"
field_sequence_without_modifications = "sequence_without_modifications"
field_secondary_structure = "secondary_structure"

class MongoTemplateRepository():
    def __init__(self):
        client = MongoClient()
        self.db = client.RNA

    def add_template(self, template):
        assert isinstance(template, Template.Template)
        tinfo = template.template_info
        assert isinstance(tinfo, Template.TemplateInfo)
        data =  {
                field_structure_id: tinfo.id,
                field_chain_id : tinfo.chain_id,
                field_sequence : template.get_sequence(),
                field_sequence_without_modifications : template.get_sequence_without_modifications(),
                "secondary_structure" : template.get_secondary_structure()
                }
        table = self.__get_templates_table()
        id = table.insert_one(data).inserted_id
        return id

    def get_all_unmodified_sequences(self):
        table = self.__get_templates_table()
        projection = [field_structure_id, field_chain_id, field_sequence_without_modifications]
        results = table.find(projection=projection)
        for result in results:
            id = result[field_structure_id] + "_" + result[field_chain_id]
            sequence = result[field_sequence_without_modifications]
            yield id, sequence

    def __get_templates_table(self):
        return self.db.templates
