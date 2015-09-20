__author__ = 'Konrad Kopciuch'

import sys
from Config import Config
from Training.TrainingDataProvider import get_train_data
from sklearn.preprocessing import Imputer
from sklearn import svm
import sklearn.cross_validation as cv


def main_svm_cross_validation(file_with_rmsd, feature_vectors_file, percentage_size_of_test_set):
    data, target = get_train_data(file_with_rmsd, feature_vectors_file)
    #data = Imputer().fit_transform(data)

    test_size = float(percentage_size_of_test_set)/100
    data_train, data_test, target_train, target_test = cv.train_test_split(
        data, target, test_size=test_size, random_state=0)

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
    if tp == 0:
        sensitivity = 0
    else:
        sensitivity = tp / float(tp + fn)

    if tn == 0:
        specifity = 0
    else:
        specifity = tn / float(tn + fp)

    print "TP: ", tp
    print "TN: ", tn
    print "FP: ", fp
    print "FN: ", fn
    print "Sensitivity: ", sensitivity
    print "Specifity: ", specifity
    print "Cross Validation score: ", clf.score(data_test, target_test)


if __name__ == '__main__':
    if(len(sys.argv)<2):
        print 'uzycie: main_svm_cross_validation.py percentage_size_of_test_set'
    else:
        percentage_size_of_test_set = int(sys.argv[1])

        cfg = Config('config.ini')
        file_with_rmsd = cfg.get_training_results_path()
        feature_vectors_file = cfg.get_feature_vectors_path()

        main_svm_cross_validation(file_with_rmsd, feature_vectors_file, percentage_size_of_test_set)
