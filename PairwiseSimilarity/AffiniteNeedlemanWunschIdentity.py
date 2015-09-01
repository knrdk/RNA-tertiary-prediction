__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from NeedlemanWunsch.Alignment import Alingment

class AffiniteNeedlemanWunschIdentity:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        nw = NeedlemanWunsch(query_sequence, template_sequence)
        nw.set_points(2, -3, -5, -2)
        nw.align()

        alignment = nw.get_alignment()
        assert isinstance(alignment, Alingment)
        return alignment.get_identity_percent()