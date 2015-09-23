__author__ = 'Konrad Kopciuch'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Repository.MongoTemplateRepository import MongoTemplateRepository

def main():
    template_repo = MongoTemplateRepository()
    training_repo = MongoTrainingTemplateRepository()

    sequences = map(lambda x: x[1], template_repo.get_all_unmodified_sequences())
    for sequence in sequences:
        y = list(training_repo.get_templates_for_sequence(sequence))
        if len(y) > 0:
            print y

if __name__ == '__main__':
    main()