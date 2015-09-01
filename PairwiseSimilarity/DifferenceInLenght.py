__author__ = 'Konrad Kopciuch'

class DifferenceInLenght:

    @staticmethod
    def get_score(query_sequence, template_id, template_sequence, template_secondary_structure):
        l1, l2 = len(query_sequence), len(template_sequence)
        if l1 + l2 == 0:
            return 0
        else:
            return abs(l1-l2) / float(l1+l2)