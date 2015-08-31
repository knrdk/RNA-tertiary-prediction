__author__ = 'Konrad Kopciuch'

class DifferenceInLenght:

    @staticmethod
    def get_score(seq1, seq2, secondary_structure_2):
        l1, l2 = len(seq1), len(seq2)
        if l1 + l2 == 0:
            return 0
        else:
            return abs(l1-l2) / float(l1+l2)