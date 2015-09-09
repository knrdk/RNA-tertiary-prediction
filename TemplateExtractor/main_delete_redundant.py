__author__ = 'Konrad Kopciuch'

from os import remove, path

from Repository.MongoTemplateRepository import MongoTemplateRepository
from Config import Config


def __delete_template(repository, template_id, template_directory):
    structure_id, chain_id = template_id.split('_')
    repository.delete_template(structure_id, chain_id)
    template_file_path = path.join(template_directory, template_id+'.pdb')
    remove(template_file_path)


def main_delete_redundant(template_directory):
    repo = MongoTemplateRepository()
    all_sequences = list(repo.get_all_unmodified_sequences())
    distinct_sequences = set(map(lambda x: x[1], all_sequences))
    grouped = [[(y[0], y[2]) for y in all_sequences if y[1] == x] for x in distinct_sequences]

    templates_to_delete = set() #zbior bo moga byc te same szablony wielokrotnie, a chcemy usunac tylko raz
    for group in grouped:
        s = sorted(group, key=lambda x: x[1]) #sortowanie po rozdzielczosci
        for x in s[1:]:
            template_id = x[0] #id w formacie: STRUCTURE_CHAIN
            templates_to_delete.add(template_id)

    print 'Szablony do usuniecia: ', len(set)

    for template_id in templates_to_delete:
        #print "usuwanie szablonu: " + template_id
        __delete_template(repo, template_id, template_directory)

if __name__ == "__main__":
    config = Config('./../config.ini')
    template_directory = config.get_template_directory()
    main_delete_redundant(template_directory)