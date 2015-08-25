__author__ = 'Konrad Kopciuch'

from SecondaryStructureParser import SecondaryStructureParser

ss = "..(((....).)).((.(...)))"
parser = SecondaryStructureParser(ss)
tree = parser.get_tree()
print tree