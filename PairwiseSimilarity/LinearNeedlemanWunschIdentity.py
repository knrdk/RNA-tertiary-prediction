__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

class LinearNeedlemanWunschIdentity:

    @staticmethod
    def get_score(seq1, seq2, secondary_structure_2):
        nw = NeedlemanWunsch(seq1, seq2)
        nw.set_points(2, -3, 0, -3.1)
        nw.align()

        alignment = nw.get_alignment()
        return alignment.get_identity_percent()