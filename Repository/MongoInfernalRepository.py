__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

field_template_id = 'template_id'
field_rfam_family_id = 'rfam_id'
field_rfam_family_score = 'rfam_score'

class MongoInfernalRepository:

    def __init__(self):
        client = MongoClient()
        self.db = client.Infernal

    def add_rfam_family_for_template(self, template_id, rfam_family_id, rfam_family_score):
        collection = self.__get_table_for_template_rfam_mapping()

        data = {
            field_template_id: template_id,
            field_rfam_family_id: rfam_family_id,
            field_rfam_family_score: rfam_family_score
        }

        id = collection.insert_one(data).inserted_id
        return id

    def get_families_for_template(self, template_id):
        collection = self.__get_table_for_template_rfam_mapping()
        query = {field_template_id : template_id}
        projection = [field_rfam_family_id, field_rfam_family_score]

        families = collection.find(filter=query, projection=projection)
        for family in families:
            family_id = family[field_rfam_family_id]
            family_score = float(family[field_rfam_family_score])
            yield family_id, family_score

    def __get_table_for_template_rfam_mapping(self):
        return self.db.template_rfam_mapping

