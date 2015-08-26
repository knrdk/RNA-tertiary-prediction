__author__ = 'Konrad Kopciuch'

from SecondaryStructureParser import SecondaryStructureParser

ss = "..(((....).)).((.(...)))"
parser = SecondaryStructureParser()
tree = parser.get_tree(ss)
print tree