__author__ = 'Konrad Kopciuch'

from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator
from Repository.MongoTemplateRepository import MongoTemplateRepository
import Utils.ThreadPool as tp
from functools import partial
from sklearn import svm
from sklearn.externals import joblib


def __load_svm(svm_file):
    return joblib.load(svm_file)

def __get_feature_vector(query_sequence, tinfo):
    template_id, template_sequence, template_secondary_structure = tinfo
    fvc = FeatureVectorCalculator()
    fv = fvc.get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure)
    return (template_id, fv)

def __get_feature_vectors(query_sequence):
    repo = MongoTemplateRepository()
    templates = list(repo.get_templates_info())

    func = partial(__get_feature_vector, query_sequence)
    pool = tp.get_thread_pool()
    vectors = pool.map(func, templates)
    return vectors

def get_templates_ranking(svm_file, query_sequence):
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



