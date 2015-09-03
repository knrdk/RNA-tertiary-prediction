__author__ = 'Konrad Kopciuch'

from SecondaryStructureParser import SecondaryStructureParser

#ss, sq = "..(((....).)).((.(...)))", "ACGUACGUACGUACGUACGUACGU"
ss, sq = ".()()", "AGCAU"
#ss, sq = ".()", "AGC"

parser = SecondaryStructureParser()
tree = parser.get_tree(ss, sq)
print tree
print tree.get_number_of_states()