__author__ = 'Konrad Kopciuch'

from Config import Config
from Training.TrainingDataProvider import get_train_data
from sklearn import svm
from sklearn.externals import joblib

def __save_svm(classifier, file):
    joblib.dump(classifier, file)

def main_svm_train(file_with_rmsd, feature_vectors_file, svm_file):
    data, target = get_train_data(file_with_rmsd, feature_vectors_file)
    clf = svm.SVC(gamma=0.015, C=10, kernel='rbf', probability=True).fit(data, target)

    __save_svm(clf, svm_file)


if __name__ == '__main__':
    cfg = Config('config.ini')
    file_with_rmsd = cfg.get_training_results_path()
    feature_vectors_file = cfg.get_feature_vectors_path()
    svm_file = 'data.svm'

    main_svm_train(file_with_rmsd, feature_vectors_file, svm_file)