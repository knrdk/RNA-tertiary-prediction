__author__ = 'Konrad Kopciuch'

from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator
from Repository.MongoTemplateRepository import MongoTemplateRepository
import Utils.ThreadPool as tp
from functools import partial
from sklearn import svm
from sklearn.externals import joblib


def __load_svm(svm_file):
    '''
    Funkcja laduje z pliku zserializowane wytrenowane SVM
    :param svm_file: sciezka do pliku z SVM
    :return: obiekt klasy sklearn.svm
    '''
    return joblib.load(svm_file)

def __get_feature_vector(query_sequence, tinfo):
    '''
    Funkcja wylicza feature vector dla sekwencji i szablonu
    :param query_sequence: sekwencja wejsciowa
    :param tinfo: trojka (TEMPLATE_ID, TEMPLATE_SEQUENCE, TEMPLATE_SECONDARY_STRUCTURE), sekwencja jest bez zmodyfikowanych
    nukleotydow
    :return: zwraca pare (TEMPLATE_ID, FEATURE VECTOR)
    '''
    template_id, template_sequence, template_secondary_structure = tinfo
    fvc = FeatureVectorCalculator()
    fv = fvc.get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure)
    return (template_id, fv)

def __get_feature_vectors(query_sequence):
    '''
    Funkcja wylicza wielowatkowo feature vector dla zadanej sekwencji i wszystkich szablonow
    :param query_sequence: sekwencja wejsciowa
    :return: lista par (TEMPLATE_ID, FEATURE VECTOR)
    '''
    repo = MongoTemplateRepository()
    templates = list(repo.get_templates_info())

    func = partial(__get_feature_vector, query_sequence)
    pool = tp.get_thread_pool()
    vectors = pool.map(func, templates)
    return vectors

def get_templates_ranking(svm_file, query_sequence):
    '''
    Funckja zwraca ranking szablonow dla danej sekwencji ktorych prawdopodobienstwo tego samego zwoju jest wieksze
    niz 0.5. Szablonu posortowane sa malejaco po prawdopodobienstwie.
    :param svm_file: Plik z wytrenowanym SVM
    :param query_sequence: sekwencja dla ktorej bedzie stworzny ranking
    :return:
    '''
    data = __get_feature_vectors(query_sequence)
    template_ids = [x[0] for x in data]
    feature_vectors = [x[1] for x in data]

    svm = __load_svm(svm_file)
    probability = svm.predict_proba(feature_vectors)
    probability_same_fold = [x[1] for x in probability]
    ranking = zip(template_ids, probability_same_fold)
    ranking_filtered = filter(lambda x: x[1] > 0.5, ranking)
    ranking_sorted = sorted(ranking_filtered, key=lambda x: x[1], reverse=True)

    return ranking_sorted



