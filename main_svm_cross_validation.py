__author__ = 'Konrad Kopciuch'

from Repository.MongoTrainingTemplateRepository import MongoTrainingTemplateRepository
from RMSD.PredictionSignificance import get_pvalue
from Config import Config
import Utils.FloatList as fl
from sklearn import svm
from sklearn import cross_validation


def get_template_id_from_filename(filename):
    return filename.split('.')[0]


def get_trainings_chains_lenght():
    repo = MongoTrainingTemplateRepository()
    return repo.get_chains_lengths()


def get_folds_dict(file_with_rmsd):
    chains_lengths = get_trainings_chains_lenght()

    output = dict()
    with open(file_with_rmsd, 'r') as f:
        for line in f:
            (query, template, rmsd) = line.split('\t')
            query_id = get_template_id_from_filename(query) #TODO: w pliku zapisywac juz id a nie filename
            template_id = get_template_id_from_filename(template)

            pvalue = get_pvalue(chains_lengths[query_id], float(rmsd))
            is_same_fold = pvalue < 0.01

            if not output.has_key(query_id):
                output[query_id] = dict()
            output[query_id][template_id] = is_same_fold
    return output


def main_cross_validation():
    cfg = Config('config.ini')
    models_rmsd_file = cfg.get_training_results_path()
    feature_vectors_file = cfg.get_feature_vectors_path()

    folds_dict = get_folds_dict(models_rmsd_file)

    data = []
    target = []

    with open(feature_vectors_file, 'r') as f:
        for line in f:
            (query, template, fv) = line.split('\t')

            query_id = get_template_id_from_filename(query)
            template_id = get_template_id_from_filename(template)

            same_fold = folds_dict[query_id][template_id]
            data.append(fl.parse_from_string(fv))
            target.append(same_fold)

    data_train, data_test, target_train, target_test = cross_validation.train_test_split(
        data, target, test_size=0.2, random_state=0)

    clf = svm.SVC(gamma=0.015, C=10, kernel='rbf', probability=True).fit(data_train, target_train)

    tp, tn, fp, fn = 0, 0, 0, 0
    for (index, data_item) in enumerate(data_test):
        predicted = clf.predict(data_item)[0]
        if predicted != target_test[index]:
            if predicted: fp += 1
            else: fn += 1
        else:
            if predicted: tp += 1
            else: tn += 1

    print("TP: %d", tp)
    print("TN: %d", tn)
    print("FP: %d", fp)
    print("FN: %d", fn)

    print clf.score(data_test, target_test)



if __name__ == '__main__':
    main_cross_validation()
