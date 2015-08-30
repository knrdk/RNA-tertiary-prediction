__author__ = 'Konrad Kopciuch'

from Repository.MongoTemplateRepository import MongoTemplateRepository

def delete_redundant():
    repo = MongoTemplateRepository()
    all_sequences = list(repo.get_all_unmodified_sequences())
    distinct_sequences = set(map(lambda x:x[1], all_sequences))
    groupped = [[(y[0],y[2]) for y in all_sequences if y[1] == x] for x in distinct_sequences]

    for group in groupped:
        s = sorted(group, key=lambda x: x[1])
        for x in s[1:]:
            structure_id, chain_id = x[0].split('_')
            repo.delete_template(structure_id, chain_id)


if __name__ == "__main__":
    delete_redundant()