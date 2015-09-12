__author__ = 'Konrad Kopciuch'

from os import remove, path, listdir
from Repository.MongoTemplateRepository import MongoTemplateRepository
from Config import Config


def __delete_template(repository, db_id):
    repository.delete_template(db_id)


def __delete_unused_template_files(repository, template_directory):
    '''
    Funkcja usuwa pliki szablonow o ktorych informacji nie ma w bazie danych
    :param repository: obiekt klasy MongoTrainingTemplateRepository
    :param template_directory: sciezka do folderu z szablonami zbioru treningowego
    :return: Funkcja nic nie zwraca
    '''
    templates_id = set(repository.get_templates_id())
    for file_path in listdir(template_directory):
        file_id = file_path.split('.')[0].upper()
        if not file_id in templates_id:
            full_path = path.join(template_directory, file_path)
            remove(full_path)
            print "usuwanie pliku szablonu: ", file_path


def main_template_delete_redundant(template_directory):
    repo = MongoTemplateRepository()
    result = repo.get_all_unmodified_sequences() #krotki: db_id, unmodified_sequence, resolution, template_id
    all_sequences = list(result) #result jest generatorem sekwencji, tworzymy liste bo bedziemy wielokrotnie po niej iterowac

    distinct_sequences = set(map(lambda x: x[1], all_sequences)) #zbior zawiera wszystkie rozne sekwencje
    grouped = [[(y[0], y[2]) for y in all_sequences if y[1] == x] for x in distinct_sequences]

    templates_to_delete = []
    for group in grouped:
        s = sorted(group, key=lambda x: x[1]) #sortowanie po rozdzielczosci, najelpsze zostaje w bazie
        for x in s[1:]:
            db_id = x[0]
            templates_to_delete.append(db_id)

    print 'Liczba szablonow do usuniecia: ', len(templates_to_delete)

    for db_id in templates_to_delete:
        print "usuwanie szablonu: " + str(db_id)
        __delete_template(repo, db_id)

    __delete_unused_template_files(repo, template_directory)

if __name__ == "__main__":
    config = Config('config.ini')
    template_directory = config.get_template_directory()
    main_template_delete_redundant(template_directory)