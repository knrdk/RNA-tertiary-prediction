__author__ = 'Konrad Kopciuch'

from AffiniteNeedlemanWunsch import AffiniteNeedlemanWunsch
from LinearNeedlemanWunsch import LinearNeedlemanWunsch
from Ribosum85NeedlemanWunsch import Ribosum85NeedlemanWunsch
from DifferenceInLenght import DifferenceInLenght

methods = [AffiniteNeedlemanWunsch,
           LinearNeedlemanWunsch,
           Ribosum85NeedlemanWunsch,
           DifferenceInLenght]

database = [
    ("GAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUC", ""),
    ("GAACGUUC", "")
]
query = "GUGUACC"

for (template_sequence, template_secondary_structure) in database:
    for method in methods:
        print method.__name__
        print method.get_score(query, template_sequence, template_secondary_structure)
    print "---"