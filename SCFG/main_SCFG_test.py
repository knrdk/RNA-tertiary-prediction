__author__ = 'Konrad Kopciuch'

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from ScoringMatrix import get_ribosum_matrices


#ss, sq = "..(((....).)).((.(...)))", "ACGUACGUACGUACGUACGUACGU"
#ss, sq = ".()()", "AGCAU"
ss, sq = ".()", "AGC"

single_matrix, double_matrix = get_ribosum_matrices()
parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
scfg = parser.get_SCFG(ss, sq)
sequence = "AAU"
score = scfg.get_score(sequence)
print score





