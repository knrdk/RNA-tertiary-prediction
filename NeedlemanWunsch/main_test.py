__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch import NeedlemanWunsch
from Alignment import Alingment

subject = "GCCGAUAUAGCUCAGUUGGUAGAGCAGCGCAUUCGUAAUGCGAAGGUCGUAGGUUCGACUCCUAUUAUCGGCACCA"
query =   "GGGGUAUCGCCAAGCGGUAAGGCACCGGAUUCUGAUUCCGGCAUUCCGAGGUUCGAAUCCUCGUACCCCAGCCA"
nw = NeedlemanWunsch(subject, query)
nw.set_points(2, -3, -5, -2)
nw.align()
score = nw.get_score()
align = nw.get_alignment()
print align.get_identity_percent()
print align
print score
