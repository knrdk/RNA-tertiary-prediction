__author__ = 'rna'

from AffiniteNeedlemanWunschIdentity import AffiniteNeedlemanWunschIdentity
from AffiniteNeedlemanWunschScore import AffiniteNeedlemanWunschScore
from LinearNeedlemanWunschIdentity import LinearNeedlemanWunschIdentity
from Ribosum85NeedlemanWunschIdentity import Ribosum85NeedlemanWunschIdentity
from Ribosum85NeedlemanWunschScore import Ribosum85NeedlemanWunschScore
from DifferenceInLenght import DifferenceInLenght
from InfernalBestFamilyScore import InfernalBestFamilyScore
from SCFGScore import SCFGScore

methods = [AffiniteNeedlemanWunschScore] #[AffiniteNeedlemanWunschIdentity]#,
           #AffiniteNeedlemanWunschScore,
           #LinearNeedlemanWunschIdentity,
           #Ribosum85NeedlemanWunschIdentity,
           #Ribosum85NeedlemanWunschScore,
           #DifferenceInLenght,
           #InfernalBestFamilyScore,
           #SCFGScore]

class FeatureVectorCalculator:

    @staticmethod
    def get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure):
        vector = []
        for method in methods:
            score = method.get_score(query_sequence, template_id, template_sequence, template_secondary_structure)
            vector.append(score)
        return vector

