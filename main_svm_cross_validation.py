__author__ = 'Konrad Kopciuch'

from Config import Config
from Training.TrainingDataProvider import get_train_data
from sklearn import svm
from sklearn import cross_validation


def main_svm_cross_validation(file_with_rmsd, feature_vectors_file):
    data, target = get_train_data(file_with_rmsd, feature_vectors_file)

    data_train, data_test, target_train, target_test = cross_validation.train_test_split(
        data, target, test_size=0.2, random_state=0)

    clf = svm.SVC(gamma=0.015, C=10, kernel='rbf', probability=True).fit(data_train, target_train)

    tp, tn, fp, fn = 0, 0, 0, 0
    predicted_test = clf.predict(data_test)
    for (target_value, predicted_value) in zip(target_test, predicted_test):
        if predicted_value != target_value:
            if predicted_value: fp += 1
            else: fn += 1
        else:
            if predicted_value: tp += 1
            else: tn += 1

    sensitivity = tp / float(tp + fn)
    specifity = tn / float(tn + fp)

    print "TP: ", tp
    print "TN: ", tn
    print "FP: ", fp
    print "FN: ", fn
    print "Sensitivity: ", sensitivity
    print "Specifity: ", specifity
    print "Cross Validation score: ", clf.score(data_test, target_test)


if __name__ == '__main__':
    cfg = Config('config.ini')
    file_with_rmsd = cfg.get_training_results_path()
    feature_vectors_file = cfg.get_feature_vectors_path()

    main_svm_cross_validation(file_with_rmsd, feature_vectors_file)
