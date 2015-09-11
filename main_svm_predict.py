__author__ = 'Konrad Kopciuch'

from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator
from Repository.MongoTemplateRepository import MongoTemplateRepository
import Utils.ThreadPool as tp
from functools import partial
from sklearn import svm
from sklearn.externals import joblib

def __load_svm(svm_file):
    return joblib.load(svm_file)

def get_feature_vector(query_sequence, tinfo):
    template_id, template_sequence, template_secondary_structure = tinfo
    print template_id
    fvc = FeatureVectorCalculator()
    fv = fvc.get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure)
    return (template_id, fv)

def get_feature_vectors(query_sequence):
    repo = MongoTemplateRepository()
    templates = list(repo.get_templates_info())

    func = partial(get_feature_vector, query_sequence)
    pool = tp.get_thread_pool()
    vectors = pool.map(func, templates)
    return vectors

def main_svm_predict(svm_file, query_sequence):
    data = get_feature_vectors(query_sequence)
    template_ids = [x[0] for x in data]
    feature_vectors = [x[1] for x in data]

    svm = __load_svm(svm_file)
    predicted = svm.predict_proba(feature_vectors)

    ranking = zip(template_ids, predicted)

    print ranking



if __name__ == '__main__':
    sequence = 'UAUCAGUUAUAUGACUGACGGAACGUGGAAUUAACCACAUGAAGUAUAACGAUGACAAUGCCGACCGUCUGGGCG'
    main_svm_predict('data.svm', sequence)