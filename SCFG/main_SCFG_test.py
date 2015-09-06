__author__ = 'Konrad Kopciuch'

from time import time

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_scoring_matrices

start_time = time()

#ss, sq = "((((((((....(.(((...(((.....)))......))))(((..(((....))).)))...(....(((((....)))))..))))))))).", "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
ss, sq = "((((........))))......(((((....)))))...............", "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
#ss, sq = ".()()()", "AGCAUGC"
#ss, sq = ".()", "AGC"
#ss = "((((((((.((((.(((.....))))))......)..)))).....(((...((((......))))...)))..))))."
#sq = "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUGGGCGAUGAGGCCCGCCCAAACUGCCCUG"
single_matrix, double_matrix = get_scoring_matrices()
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
scfg = parser.get_SCFG(ss, sq)
sequence = "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
#sequence = "AGCGAGCGAGCG"
scfg.align(sequence)
score = scfg.get_score()
print score
t,q = scfg.get_alingment()
print t
print q

end_time = time()
print "Time: ", end_time-start_time




