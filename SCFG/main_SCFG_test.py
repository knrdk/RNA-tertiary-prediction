__author__ = 'Konrad Kopciuch'

from SecondaryStructureParser import SecondaryStructureParser

ss = "..(((....).)).((.(...)))"
sq = "ACGUACGUACGUACGUACGUACGU"
parser = SecondaryStructureParser()
tree = parser.get_tree(ss, sq)
print tree