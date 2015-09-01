__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

ribosum85_matrix = {
    'A': {'A': 1.88, 'C': -1.23, 'G': -0.84, 'U': -0.83},
    'C': {'C': -0.95, 'G': -1.64, 'U':-0.57},
    'G':{'G': 0.82, 'U': -1.03},
    'U': {'U': 1.31}}

class Ribosum85NeedlemanWunschIdentity:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        nw = NeedlemanWunsch(query_sequence, template_sequence)
        nw.set_points(2, -1.64, -3, -1)
        nw.set_substitution_matrix(ribosum85_matrix)
        nw.align()

        alignment = nw.get_alignment()
        return alignment.get_identity_percent()