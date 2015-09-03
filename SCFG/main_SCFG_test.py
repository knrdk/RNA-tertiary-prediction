__author__ = 'Konrad Kopciuch'

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser

ss, sq = "..(((....).)).((.(...)))", "ACGUACGUACGUACGUACGUACGU"
#ss, sq = ".()()", "AGCAU"
#ss, sq = ".()", "AGC"


parser = SecondaryStructureToSCFGParser()
parser.get_SCFG(ss, sq)