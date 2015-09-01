__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

class LinearNeedlemanWunschIdentity:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        nw = NeedlemanWunsch(query_sequence, template_sequence)
        nw.set_points(2, -3, 0, -3.1)
        nw.align()

        alignment = nw.get_alignment()
        return alignment.get_identity_percent()