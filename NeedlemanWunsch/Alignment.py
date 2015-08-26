__author__ = 'Konrad Kopciuch'

class Alingment:
    def __init__(self, sequence_x, sequence_y):
        assert isinstance(sequence_x, str)
        assert isinstance(sequence_y, str)
        assert len(sequence_x) == len(sequence_y)

        self.x = sequence_x
        self.y = sequence_y
        self.length = len(self.x)

    def get_identity_percent(self):
        identical = 0.0
        for i in range(self.length):
            if self.x[i] == self.y[i]:
                identical+=1
        return identical/self.length

