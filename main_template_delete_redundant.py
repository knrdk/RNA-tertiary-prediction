__author__ = 'Konrad Kopciuch'

from os import remove, path

from Repository.MongoTemplateRepository import MongoTemplateRepository
from Config import Config


def __delete_template(repository, template_id):
    repository.delete_template(template_id)
    #TODO: usuwanie zbednych plikow szablonow


def main_template_delete_redundant(template_directory):
    repo = MongoTemplateRepository()
    result = repo.get_all_unmodified_sequences() #krotki: template_id, unmodified_sequence, resolution
    all_sequences = list(result) #result jest generatorem sekwencji, tworzymy liste bo bedziemy wielokrotnie po niej iterowac

    distinct_sequences = set(map(lambda x: x[1], all_sequences)) #zbior zawiera wszystkie rozne sekwencje
    grouped = [[(y[0], y[2]) for y in all_sequences if y[1] == x] for x in distinct_sequences]

    templates_to_delete = []
    #w bazie moze byc wiele dokumentow z takim samym template_id
    for group in grouped:
        s = sorted(group, key=lambda x: x[1]) #sortowanie po rozdzielczosci, najelpsze zostaje w bazie
        for x in s[1:]:
            db_id = x[0]
            templates_to_delete.append(db_id)

    print 'Liczba szablonow do usuniecia: ', len(templates_to_delete)

    for db_id in templates_to_delete:
        print "usuwanie szablonu: " + str(db_id
        __delete_template(repo, db_id)

if __name__ == "__main__":
    config = Config('./../config.ini')
    template_directory = config.get_template_directory()
    main_template_delete_redundant(template_directory)