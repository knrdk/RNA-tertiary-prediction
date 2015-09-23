__author__ = 'Konrad Kopciuch'

from Config import Config
from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Repository.MongoTemplateRepository import MongoTemplateRepository
from Training.DeleteTrainingTemplate import delete_template, delete_unused_template_files

def main(training_template_directory):
    template_repo = MongoTemplateRepository()
    training_repo = MongoTrainingTemplateRepository()

    sequences = map(lambda x: x[1], template_repo.get_all_unmodified_sequences())
    for sequence in sequences:
        for db_id in training_repo.get_templates_for_sequence(sequence):
            print str(db_id)
            delete_template(training_repo, db_id)

    delete_unused_template_files(training_repo, training_template_directory)


if __name__ == '__main__':
    config = Config('config.ini')
    training_template_directory = config.get_training_set_directory()
    main(training_template_directory)
