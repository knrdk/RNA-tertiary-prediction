__author__ = 'Konrad Kopciuch'

import sys
from Config import Config
from Training.TrainingDataProvider import get_train_data
from sklearn import svm
import sklearn.cross_validation as cv
import math


def calculate_mcc(tp, fp, tn, fn):
    nominator = tp*tn - fp*fn
    denomiator_squared = (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)
    denomiantor = math.sqrt(denomiator_squared)

    if denomiantor == 0:
        return nominator

    return nominator/denomiantor


def calculate_specifity(fp, tn):
    if tn == 0:
        return 0
    else:
        return tn / float(tn + fp)


def calculate_senstivity(tp, fn):
    if tp == 0:
        return 0
    else:
        return tp / float(tp + fn)


def main_svm_cross_validation(file_with_rmsd, feature_vectors_file, percentage_size_of_test_set):
    data, target = get_train_data(file_with_rmsd, feature_vectors_file)

    test_size = float(percentage_size_of_test_set)/100
    data_train, data_test, target_train, target_test = cv.train_test_split(
        data, target, test_size=test_size)

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

    sensitivity = calculate_senstivity(tp, fn)
    specifity = calculate_specifity(fp, tn)
    mcc = calculate_mcc(tp, fp, tn, fn)

    print "TP: ", tp
    print "TN: ", tn
    print "FP: ", fp
    print "FN: ", fn
    print "Sensitivity: ", sensitivity
    print "Specifity: ", specifity
    print "MCC: ", mcc
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
