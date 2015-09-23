__author__ = 'Konrad Kopciuch'


from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from Config import Config
from Training.DeleteTrainingTemplate import delete_template, delete_unused_template_files

def main_delete_redundant(training_template_directory):
    '''
    Funkcja usuwa te szablony ktorych sekwencja sie powtarza, pozostawiajac jeden z nich
    :param training_template_directory: Sciezka do folderu z szablonami zbioru treningowego
    :return:
    '''
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
        delete_template(repo, db_id)

    delete_unused_template_files(repo, training_template_directory)


if __name__ == "__main__":
    config = Config('config.ini')
    training_template_directory = config.get_training_set_directory()
    main_delete_redundant(training_template_directory)