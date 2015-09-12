__author__ = 'Konrad Kopciuch'

import time

from FeatureVectorCalculator import FeatureVectorCalculator
from Repository.MongoTemplateRepository import MongoTemplateRepository


def main():
    repo = MongoTemplateRepository()
    templates = repo.get_templates_info()
    query = "UGGGAGGUCGUCUAACGGUAGGACGGCGGACUCUGGAUCCGCUGGUGGAGGUUCGAGUCCUCCCCUCCCAGCCA"

    all_vectors = []
    for (template_id, template_sequence, template_secondary_structure) in templates:
        fv = FeatureVectorCalculator.get_feature_vector(query, template_id, template_sequence, template_secondary_structure)
        all_vectors.append((template_id, fv))
        print template_id, fv

    x = sorted(all_vectors, key=lambda z: z[1][0], reverse=True)
    for best in x[:5]:
        print best

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))