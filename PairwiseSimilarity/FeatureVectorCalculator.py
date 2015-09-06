__author__ = 'rna'

from AffiniteNeedlemanWunschIdentity import AffiniteNeedlemanWunschIdentity
from AffiniteNeedlemanWunschScore import AffiniteNeedlemanWunschScore
from DifferenceInLenght import DifferenceInLenght
from SCFGScore import SCFGScore

methods = [AffiniteNeedlemanWunschIdentity,
           AffiniteNeedlemanWunschScore,
           #LinearNeedlemanWunschIdentity,
           #Ribosum85NeedlemanWunschIdentity,
           #Ribosum85NeedlemanWunschScore,
           DifferenceInLenght,
           #InfernalBestFamilyScore,
           #InfernalAlignmentIdentity,
           SCFGScore]

class FeatureVectorCalculator:

    @staticmethod
    def get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure):
        vector = []
        for method in methods:
            score = method.get_score(query_sequence, template_id, template_sequence, template_secondary_structure)
            vector.append(score)
        return vector

