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
        '''
        Funckja dodaje informacje o szablonie do bazy danych
        :param template: obiekt klasy Template.Template
        :return: id w bazie danych
        '''
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
        '''
        Funkcja zwraca wszystkie niemodyfikownae sekwencje znajdujace sie w bazie szablonow
        :return: Funkcja zwraca krotke 4 elementowa, jej kolejnymi elementami sa:
        db_id, sekwencja bez modyfikacji, rozdzielczosc, template_id
        '''
        collection = self.__get_templates_collection()
        projection = ['_id', field_sequence_without_modifications, field_resolution, field_structure_id, field_chain_id]
        results = collection.find(projection=projection)
        for result in results:
            db_id = result['_id']
            sequence = str(result[field_sequence_without_modifications])
            resolution = float(result[field_resolution])
            structure_id = str(result[field_structure_id])
            chain_id = str(result[field_chain_id])
            template_id = structure_id + '_' + chain_id
            yield db_id, sequence, resolution, template_id

    def get_template_info(self, template_id):
        '''
        Funckja zwraca informacje o szablonie o wybranych identyfikatorze
        :param template_id: identyfikator w formacie STRUCTURE_CHAIN
        :return: funkcja zwraca trojke: (sequence, unmodified sequence, secondary_structure)
        '''
        structure_id, chain_id = template_id.split('_')
        collection = self.__get_templates_collection()
        projection = [field_sequence, field_sequence_without_modifications, field_secondary_structure]
        filter = {field_structure_id: structure_id, field_chain_id: chain_id}

        result = collection.find_one(filter=filter, projection = projection)
        sequence = str(result[field_sequence])
        unmodified_sequence = str(result[field_sequence_without_modifications])
        secondary_structure = str(result[field_secondary_structure])

        return (sequence, unmodified_sequence, secondary_structure)

    def get_templates_info(self):
        '''
        Funkcja zwraca informacje o szablonach, potrzebne do wyliczenia FeatureVector
        :return: lista trojek: (template_id, unmodified sequence, secondary_structure)
        '''
        collection = self.__get_templates_collection()
        projection = [field_structure_id, field_chain_id, field_sequence_without_modifications, field_secondary_structure]
        results = collection.find(projection=projection)
        for result in results:
            template_id = str(result[field_structure_id] + "_" + result[field_chain_id])
            sequence = str(result[field_sequence_without_modifications])
            secondary_structure = str(result[field_secondary_structure])
            yield (template_id, sequence, secondary_structure)

    def get_structures_id(self):
        collection = self.__get_templates_collection()
        projection = [field_structure_id]
        results = collection.find(projection=projection)
        output = set()
        for result in results:
            structure_id = str(result[field_structure_id])
            output.add(structure_id)
        return output

    def delete_template(self, db_id):
        '''
        Funckcja usuwa informacje o szablonie z bazy danych
        :param db_id identyfikator szablonu w bazie danych
        :return: Funkcja nic nie zwraca
        '''
        #structure_id, chain_id = template_id.split('_')
        collection = self.__get_templates_collection()
        filter = {'_id': db_id}
        collection.remove(filter)

    def __get_templates_collection(self):
        '''
        :return: Funckcja zwraca kolekcje szablonow w bazie danych
        '''
        return self.db.templates
