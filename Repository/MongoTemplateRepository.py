__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

from Utils import Template

field_structure_id = "structure_id"
field_chain_id = "chain_id"
field_sequence = "sequence"
field_sequence_without_modifications = "sequence_without_modifications"
field_secondary_structure = "secondary_structure"
field_resolution = "resolution"

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
                field_secondary_structure : template.get_secondary_structure(),
                field_resolution : tinfo.resolution
                }
        collection = self.__get_templates_collection()
        id = collection.insert_one(data).inserted_id
        return id

    def get_all_unmodified_sequences(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id, field_sequence_without_modifications, field_resolution]
        results = collection.find(projection=projection)
        for result in results:
            id = result[field_structure_id] + "_" + result[field_chain_id]
            sequence = str(result[field_sequence_without_modifications])
            resolution = float(result[field_resolution])
            yield id, sequence, resolution

    def get_templates_info(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id, field_sequence_without_modifications, field_secondary_structure]
        results = collection.find(projection=projection)
        for result in results:
            id = str(result[field_structure_id] + "_" + result[field_chain_id])
            sequence = str(result[field_sequence_without_modifications])
            secondary_structure = str(result[field_secondary_structure])
            yield (id, sequence, secondary_structure)

    def delete_template(self, structure_id, chain_id):
        collection = self.__get_templates_collection()
        collection.remove({field_structure_id: structure_id, field_chain_id: chain_id})

    def __get_templates_collection(self):
        return self.db.templates
