__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

class AffiniteNeedlemanWunschScore:

    @staticmethod
    def get_score(seq1, seq2, secondary_structure_2):
        alignment_score = AffiniteNeedlemanWunschScore.__get_nw_score(seq1, seq2)
        seq1_score = AffiniteNeedlemanWunschScore.__get_nw_score(seq1, seq1)
        seq2_score = AffiniteNeedlemanWunschScore.__get_nw_score(seq2, seq2)
        maximum = max(seq1_score, seq2_score)

        if maximum == 0:
            return 1
        else:
            return float(alignment_score) / maximum

    @staticmethod
    def __get_nw_score(seq1, seq2):
        nw = NeedlemanWunsch(seq1, seq2)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()
        return score