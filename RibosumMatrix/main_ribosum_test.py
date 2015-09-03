__author__ = 'Konrad Kopciuch'

from RibosumParser import RibosumParser

path = "C:/RIBOSUM85.mat"
parser = RibosumParser(path)

matrix = parser.get_single_matrix()
print matrix

d_matrix = parser.get_double_matrix()
print d_matrix


