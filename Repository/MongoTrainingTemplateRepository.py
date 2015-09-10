__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

from Utils import Template

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

    def get_all_sequences(self):
        collection = self.__get_templates_collection()
        projection = ['_id', field_sequence]
        results = collection.find(projection=projection)
        for result in results:
            db_id = result['_id']
            sequence = str(result[field_sequence])
            yield db_id, sequence

    def get_all_templates_id(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id]
        results = collection.find(projection=projection)
        for result in results:
            structure_id = str(result[field_structure_id])
            chain_id = str(result[field_chain_id])
            template_id = structure_id + '_' + chain_id
            yield template_id

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

    def delete_template(self, db_id):
        collection = self.__get_templates_collection()
        collection.remove({'_id': db_id})

    def __get_templates_collection(self):
        return self.db.training_templates

    def __get_template_id(self, structure_id, chain_id):
        return str(structure_id) + '_' + str(chain_id)