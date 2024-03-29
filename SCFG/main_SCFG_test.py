__author__ = 'Konrad Kopciuch'

from time import time

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_scoring_matrices

start_time = time()

ss, sq = "(((....(.(((...(((.....)))......))))(((..(((....))).)))...(....(((((....)))))..))))", "UCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAG"
#ss, sq = "((((........))))......(((((....)))))...............", "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
#ss, sq = ".()()()", "AGCAUGC"
#ss, sq = ".()", "AGC"
#ss = "((((((((.((((.(((.....))))))......)..)))).....(((...((((......))))...)))..))))."
#sq = "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUGGGCGAUGAGGCCCGCCCAAACUGCCCUG"
single_matrix, double_matrix = get_scoring_matrices('./../config.ini')
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
scfg = parser.get_SCFG(ss, sq)
#sequence = "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
sequence = "GGCGAUGAGGCCCGCCCAAACUGCCCU"
#sequence = "AGCGAGCGAGCG"
scfg.align(sequence)
score = scfg.get_score()
print score
algn = scfg.get_alignment()
print algn

end_time = time()
print "Time: ", end_time-start_time




