__author__ = 'Konrad Kopciuch'

from pymongo import MongoClient

import Template

field_template_id = "template_id"
field_self_score = "score"


class MongoSCFGRepository():
    def __init__(self):
        client = MongoClient()
        self.db = client.RNA

    def add_scfg_self_score(self, template_id, self_score):
        '''
        Funkcja dodaje do bazy danych wynik dopasowania sekwencji to SCFG utworzonego na podstawie tej sekwencji
        :param template_id: Id szablonu z ktorego pochodzi sekwencja, format: STRUCTURE_CHAIN
        :param self_score: wynik dopasowania sekwencji do swojej SCFG
        :return: id wstawionego rekordu
        '''
        data =  {
                field_template_id: template_id,
                field_self_score : self_score
                }
        collection = self.__get_collection()
        id = collection.insert_one(data).inserted_id
        return id

    def get_scfg_self_score(self, template_id):
        '''
        Funkcja zwraca wartosc dopasowania sekwencji do SCFG utworzonej na podstawie tej sekwencji dla podanego
        identyfikatora szablonu
        :param template_id: Identyfikator szablon w formacie STRUCTURE_CHAIN
        :return: Wartosc dopasowania jesli istnieje w bazie, None w przeciwnym przypadku
        '''
        collection = self.__get_collection()
        filter = {field_template_id: template_id}
        projection = [field_self_score]
        results = collection.find(filter=filter, projection=projection, limit=1)
        for result in results:
            return float(result[field_self_score])
        return None

    def __get_collection(self):
        return self.db.scfg