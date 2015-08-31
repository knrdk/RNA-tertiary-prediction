__author__ = 'Konrad Kopciuch'

from AffiniteNeedlemanWunschIdentity import AffiniteNeedlemanWunschIdentity
from AffiniteNeedlemanWunschScore import AffiniteNeedlemanWunschScore
from LinearNeedlemanWunschIdentity import LinearNeedlemanWunschIdentity
from Ribosum85NeedlemanWunschIdentity import Ribosum85NeedlemanWunschIdentity
from Ribosum85NeedlemanWunschScore import Ribosum85NeedlemanWunschScore
from DifferenceInLenght import DifferenceInLenght

methods = [AffiniteNeedlemanWunschIdentity,
           AffiniteNeedlemanWunschScore,
           LinearNeedlemanWunschIdentity,
           Ribosum85NeedlemanWunschIdentity,
           Ribosum85NeedlemanWunschScore,
           DifferenceInLenght]

database = [
    ("GAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUC", None),
    ("GAACGUUC", None),
    ("UGGGAGGUCGUCUAACGGUAGGACGGCGGACUCUGGAUCCGCUGGUGGAGGUUCGAGUCCUCCCCUCCCAGCCA", None)
]
query = "GGCCAGGUAGCUCAGUUGGUAGAGCACUGGACUGAAAAUCCAGGUGUCGGCGGUUCGAUUCCGCCCCUGGCCA"

for (template_sequence, template_secondary_structure) in database:
    for method in methods:
        print method.__name__
        print method.get_score(query, template_sequence, template_secondary_structure)
    print "---"