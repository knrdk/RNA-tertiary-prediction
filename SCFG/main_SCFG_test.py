__author__ = 'Konrad Kopciuch'

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_ribosum_matrices


ss, sq = "((((((((....(.(((...(((.....)))......))))(((..(((....))).)))...(....(((((....)))))..))))))))).", \
         "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"

#ss, sq = "((((........))))......(((((....)))))...............", "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
#ss, sq = ".()()", "AGCAU"
#ss, sq = ".()", "AGC"
print "GET_MATRICES"
single_matrix, double_matrix = get_ribosum_matrices()
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
print "GET_SCFG"
scfg = parser.get_SCFG(ss, sq)
print "ALIGN_TO_SCFG"
sequence = "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
score = scfg.get_score(sequence)
print score





