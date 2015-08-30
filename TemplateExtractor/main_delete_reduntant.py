__author__ = 'Konrad Kopciuch'

from Repository.MongoTemplateRepository import MongoTemplateRepository

def delete():
    repo = MongoTemplateRepository()
    all_sequences = repo.get_all_unmodified_sequences()
    distinct_sequences = map(lambda x:x[1], all_sequences)

    print len(all_sequences), len(distinct_sequences)