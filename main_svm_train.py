__author__ = 'Konrad Kopciuch'

from Config import Config
from Training.TrainingDataProvider import get_train_data
import sys
import numpy as np
from sklearn import svm
from sklearn.externals import joblib

def __save_svm(classifier, file):
    '''
    Funkcja serializuje i zapisuje obiekt klasy sklearn.svm do pliku
    :param classifier: wytrenowany svm
    :param file: plik w ktorym zostanie zapisany svm
    :return: funkcja nic nie zwraca
    '''
    joblib.dump(classifier, file)

def main_svm_train(file_with_rmsd, feature_vectors_file, svm_file):
    '''
    Funkcja na podstawie plikow z odlegloscia RMSD dla par (szablon, sekwencja) i feature vector dla takich samych par
    trenuje SVM i zapisuje go do pliku
    :param file_with_rmsd: Plik z wartosciami RMSD, rezultat wykonania programu main_trainig_cross_rmsd.py
    :param feature_vectors_file: plik z feature vector, rezultat wykonania main_training_cross_feature_vector.py
    :param svm_file: sciezka do pliku w ktorym zostanie zapisany svm
    :return: funkcja nic nie zwraca
    '''
    data, target = get_train_data(file_with_rmsd, feature_vectors_file)
    X = np.asarray(data)
    clf = svm.SVC(gamma=0.015, C=10, kernel='rbf', probability=True).fit(X, target)

    __save_svm(clf, svm_file)


if __name__ == '__main__':
    cfg = Config('config.ini')
    file_with_rmsd = cfg.get_training_results_path()
    feature_vectors_file = cfg.get_feature_vectors_path()
    svm_file = cfg.get_svm_file()

    main_svm_train(file_with_rmsd, feature_vectors_file, svm_file)