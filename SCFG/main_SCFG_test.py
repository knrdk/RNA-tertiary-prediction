__author__ = 'Konrad Kopciuch'

from ConfigParser import ConfigParser

from SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from RibosumMatrix.RibosumParser import RibosumParser

'''
ss, sq = "..(((....).)).((.(...)))", "ACGUACGUACGUACGUACGUACGU"
#ss, sq = ".()()", "AGCAU"
#ss, sq = ".()", "AGC"


parser = SecondaryStructureToSCFGParser()
parser.get_SCFG(ss, sq)
'''

def get_ribosum_matrix_path(config_path):
    config = ConfigParser()
    config.read(config_path)
    section = 'Ribosum'
    matrix_path = "matrixpath"
    return config.get(section, matrix_path)

ribosum_matrix_path = get_ribosum_matrix_path("config.ini")
parser = RibosumParser(ribosum_matrix_path)
sm = parser.get_single_matrix()
dm = parser.get_double_matrix()

print sm
print dm