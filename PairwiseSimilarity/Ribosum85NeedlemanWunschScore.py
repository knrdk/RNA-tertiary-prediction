__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

ribosum85_matrix = {
    'A': {'A': 1.88, 'C': -1.23, 'G': -0.84, 'U': -0.83},
    'C': {'C': -0.95, 'G': -1.64, 'U':-0.57},
    'G':{'G': 0.82, 'U': -1.03},
    'U': {'U': 1.31}}

class Ribosum85NeedlemanWunschScore:

    @staticmethod
    def get_score(seq1, seq2, secondary_structure_2):
        alignment_score = Ribosum85NeedlemanWunschScore.__get_nw_score(seq1, seq2)
        seq1_score = Ribosum85NeedlemanWunschScore.__get_nw_score(seq1, seq1)
        seq2_score = Ribosum85NeedlemanWunschScore.__get_nw_score(seq2, seq2)
        maximum = max(seq1_score, seq2_score)

        if maximum == 0:
            return 1
        else:
            return float(alignment_score) / maximum

    @staticmethod
    def __get_nw_score(seq1, seq2):
        nw = NeedlemanWunsch(seq1, seq2)
        nw.set_points(2, -1.64, -3, -1)
        nw.set_substitution_matrix(ribosum85_matrix)
        nw.align()
        score = nw.get_score()
        return score