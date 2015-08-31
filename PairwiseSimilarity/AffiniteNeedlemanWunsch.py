__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from NeedlemanWunsch.Alignment import Alingment

class AffiniteNeedlemanWunsch:

    @staticmethod
    def get_score(seq1, seq2, secondary_structure_2):
        nw = NeedlemanWunsch(seq1, seq2)
        nw.set_points(2, -3, -5, -2)
        nw.align()

        alignment = nw.get_alignment()
        assert isinstance(alignment, Alingment)
        return alignment.get_identity_percent()