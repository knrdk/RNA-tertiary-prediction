__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

class MongoInfernalRepository:

    def __init__(self):
        client = MongoClient()
        self.db = client.Infernal

    def set_rfam_id_for_template(self, rfam_id, structure_id, chain_id):
        table = self.__get_table_for_template_rfam_mapping()


    def __get_table_for_template_rfam_mapping(self):
        return self.db.template_rfam_mapping

