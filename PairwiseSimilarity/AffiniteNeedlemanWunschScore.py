__author__ = 'Konrad Kopciuch'

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch

class AffiniteNeedlemanWunschScore:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        alignment_score = AffiniteNeedlemanWunschScore.__get_nw_score(query_sequence, template_sequence)
        seq1_score = AffiniteNeedlemanWunschScore.__get_nw_score(query_sequence, query_sequence)
        seq2_score = AffiniteNeedlemanWunschScore.__get_nw_score(template_sequence, template_sequence)
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