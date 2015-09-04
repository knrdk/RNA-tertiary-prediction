__author__ = 'Konrad Kopciuch'

from os import remove, path

from Repository.MongoTemplateRepository import MongoTemplateRepository
from Config import Config


def delete_template(repository, template_id):
    config = Config()
    structure_id, chain_id = template_id.split('_')
    repository.delete_template(structure_id, chain_id)
    template_file_path = path.join(config.get_template_directory(), template_id+'.pdb')
    print template_file_path
    remove(template_file_path)


def delete_redundant():
    repo = MongoTemplateRepository()
    all_sequences = list(repo.get_all_unmodified_sequences())
    distinct_sequences = set(map(lambda x:x[1], all_sequences))
    groupped = [[(y[0],y[2]) for y in all_sequences if y[1] == x] for x in distinct_sequences]

    for group in groupped:
        s = sorted(group, key=lambda x: x[1]) #sortowanie po rozdzielczosci
        for x in s[1:]:
            template_id = x[0] #id w formacie: STRUCTURE_CHAIN
            print "usuwanie szablonu: " + template_id
            delete_template(repo, template_id)


if __name__ == "__main__":
    delete_redundant()