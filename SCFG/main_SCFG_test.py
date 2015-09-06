__author__ = 'Konrad Kopciuch'

from time import time

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_scoring_matrices

start_time = time()

#ss, sq = "((((((((....(.(((...(((.....)))......))))(((..(((....))).)))...(....(((((....)))))..))))))))).", "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
#ss, sq = "((((........))))......(((((....)))))...............", "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
#ss, sq = ".()()", "AGCAU"
ss, sq = ".()", "AGC"
#ss = "((((((((.((((.(((.....))))))......)..)))).....(((...((((......))))...)))..))))."
#sq = "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUGGGCGAUGAGGCCCGCCCAAACUGCCCUG"
print "GET_MATRICES"
single_matrix, double_matrix = get_scoring_matrices()
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
print "GET_SCFG"
scfg = parser.get_SCFG(ss, sq)
print "ALIGN_TO_SCFG"
sequence = "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
#sequence = "AGCG"
scfg.align(sequence)
score = scfg.get_score()
print score
scfg.get_alingment()

end_time = time()
print "Time: ", end_time-start_time




