__author__ = 'Konrad Kopciuch'

from os import remove, listdir, path

def delete_template(repository, db_id):
    '''
    Funckja usuwa z bazy danych informacje o szablonie
    :param repository: obiekt klasy MongoTrainingTemplateRepository
    :param db_id: identyfikator w bazie danych szablonu do usuniecia
    :return:
    '''
    repository.delete_template(db_id)

def delete_unused_template_files(repository, template_directory):
    '''
    Funkcja usuwa pliki szablonow o ktorych informacji nie ma w bazie danych
    :param repository: obiekt klasy MongoTrainingTemplateRepository
    :param template_directory: sciezka do folderu z szablonami zbioru treningowego
    :return: Funkcja nic nie zwraca
    '''
    templates_id = set(repository.get_all_templates_id())
    for file_path in listdir(template_directory):
        file_id = file_path.split('.')[0].upper()
        if not file_id in templates_id:
            full_path = path.join(template_directory, file_path)
            remove(full_path)
            print "usuwanie pliku szablonu: ", file_path
