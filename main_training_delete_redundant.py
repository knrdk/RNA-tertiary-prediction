__author__ = 'Konrad Kopciuch'

from os import remove, listdir, path

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Config import Config


def __delete_template(repository, db_id):
    '''
    Funckja usuwa z bazy danych informacje o szablonie
    :param repository: obiekt klasy MongoTrainingTemplateRepository
    :param db_id: identyfikator w bazie danych szablonu do usuniecia
    :return:
    '''
    repository.delete_template(db_id)

def __delete_unused_template_files(repository, template_directory):
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

def main_delete_redundant(template_directory):
    repo = MongoTrainingTemplateRepository()
    all_sequences = list(repo.get_all_sequences())
    distinct_sequences = set(map(lambda x: x[1], all_sequences))
    grouped = [[y[0] for y in all_sequences if y[1] == x] for x in distinct_sequences]
    templates_to_delete = []
    for group in grouped:
        for db_id in group[1:]:
            templates_to_delete.append(db_id)

    for db_id in templates_to_delete:
        print "usuwanie szablonu: " + str(db_id)
        __delete_template(repo, db_id)

    __delete_unused_template_files(repo, template_directory)


if __name__ == "__main__":
    config = Config('config.ini')
    template_directory = config.get_training_set_directory()
    main_delete_redundant(template_directory)