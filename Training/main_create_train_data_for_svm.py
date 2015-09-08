__author__ = 'Konrad Kopciuch'

from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator
from Config import Config

def __parse_fv_from_file(fv):
    x = list(fv.split(';'))
    return map(lambda x: float(x), x)


def main():
    cfg = Config('./../config.ini')
    feature_vectors_file = cfg.get_feature_vectors_path()

    with open(feature_vectors_file, 'r') as f:
        for line in f:
            (template, query, fv) = line.split('\t')
            print template, query, __parse_fv_from_file(fv)


if __name__ == '__main__':
    main()
