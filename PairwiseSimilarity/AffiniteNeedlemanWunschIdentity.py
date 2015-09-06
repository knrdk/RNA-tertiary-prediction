__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from Utils.Alignment import Alignment

class AffiniteNeedlemanWunschIdentity:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        nw = NeedlemanWunsch(template_sequence, query_sequence)
        nw.set_points(2, -3, -5, -2)
        nw.align()

        alignment = nw.get_alignment()
        assert isinstance(alignment, Alignment)
        return alignment.get_identity_percent()