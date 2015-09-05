__author__ = 'Konrad Kopciuch'

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_ribosum_matrices

'''
ss, sq = "((((((((....(.(((...(((.....)))......))))(((..(((....))).)))...(....(((((....)))))..))))))))).", \
         "GGCUUAUCAAGAGAGGUGGAGGGACUGGCCCGACGAAACCCGGCAACCAGAAAUGGUGCCAAUUCCUGCAGCGGAAACGUUGAAAGAUGAGCCG"
''' #__is_first_and_last_basepair - recursion depth exceeded

ss, sq = "((((........))))......(((((....)))))...............", \
         "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
#ss, sq = ".()()", "AGCAU"
#ss, sq = ".()", "AGC"

single_matrix, double_matrix = get_ribosum_matrices()
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
scfg = parser.get_SCFG(ss, sq)
sequence = "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
score = scfg.get_score(sequence)
print score





