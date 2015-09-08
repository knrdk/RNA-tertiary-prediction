__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

import Template

field_structure_id = "structure_id"
field_chain_id = "chain_id"
field_sequence = "sequence"


class MongoTrainingTemplateRepository():
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
                field_sequence : template.get_sequence_without_modifications(),
                }
        collection = self.__get_templates_collection()
        id = collection.insert_one(data).inserted_id
        return id

    def get_all_unmodified_sequences(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id, field_sequence]
        results = collection.find(projection=projection)
        for result in results:
            template_id = self.__get_template_id(result[field_structure_id], result[field_chain_id])
            sequence = str(result[field_sequence])
            resolution = 0
            yield template_id, sequence, resolution

    def get_chains_lengths(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id, field_sequence]
        results = collection.find(projection=projection)
        out = dict()
        for result in results:
            id = self.__get_template_id(result[field_structure_id], result[field_chain_id])
            length = len(result[field_sequence])
            out[id] = length
        return out

    def delete_template(self, structure_id, chain_id):
        collection = self.__get_templates_collection()
        collection.remove({field_structure_id: structure_id, field_chain_id: chain_id})

    def __get_templates_collection(self):
        return self.db.training_templates

    def __get_template_id(self, structure_id, chain_id):
        return str(structure_id) + '_' + str(chain_id)