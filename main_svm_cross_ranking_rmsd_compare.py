__author__ = 'Konrad Kopciuch'

import sys
from Config import Config
from Training.TrainingDataProvider import get_train_data
from sklearn import svm
import sklearn.cross_validation as cv
'''

def main_svm_cross_validation(file_with_rmsd, feature_vectors_file):
    ntemplate, ntraining = 444, 68

    data, target = get_train_data(file_with_rmsd, feature_vectors_file)

    with open(file_with_rmsd, 'r') as rmsd_file:



    data_train, data_test, target_train, target_test = 0,0,0,0

    clf = svm.SVC(gamma=0.015, C=10, kernel='rbf', probability=True).fit(data_train, target_train)



if __name__ == '__main__':
        cfg = Config('config.ini')
        file_with_rmsd = cfg.get_training_results_path()
        feature_vectors_file = cfg.get_feature_vectors_path()

        main_svm_cross_validation(file_with_rmsd, feature_vectors_file)
'''