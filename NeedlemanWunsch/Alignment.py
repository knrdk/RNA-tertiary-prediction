__author__ = 'Konrad Kopciuch'

class Alingment:
    def __init__(self, sequence_x, sequence_y):
        assert isinstance(sequence_x, str)
        assert isinstance(sequence_y, str)
        assert len(sequence_x) == len(sequence_y)

        self.x = sequence_x
        self.y = sequence_y
        self.length = len(self.x)
        self.x_description = ''
        self.y_description = ''

    def get_identity_percent(self):
        identical = 0.0
        for i in range(self.length):
            if self.x[i] == self.y[i]:
                identical+=1
        return identical/self.length

    def set_sequence_x_description(self, description):
        self.x_description = description

    def set_sequence_y_description(self, description):
        self.y_description = description

    def __get_length_without_gap(self, sequence):
        i=0
        for c in sequence:
            if c != '-':
                i+=1
        return i

    def get_sequence_x(self):
        z = ''
        for c in self.x:
            if c != '-':
                z = z + c
        return z

    def get_sequence_y(self):
        z = ''
        for c in self.y:
            if c != '-':
                z = z + c
        return z

    def change_sequence_x(self, new_sequence):
        assert len(new_sequence) == self.__get_length_without_gap(self.x)
        z = ''
        i = 0
        for c in self.x:
            if c == '-':
                z = z + '-'
            else:
                z = z + new_sequence[i]
                i+=1
        self.x = z

    def change_sequence_y(self, new_sequence):
        assert len(new_sequence) == self.__get_length_without_gap(self.y)
        z = ''
        i = 0
        for c in self.y:
            if c == '-':
                z = z + '-'
            else:
                z = z + new_sequence[i]
                i+=1
        self.y = z

    def __str__(self):
        line1 = '>'+self.x_description
        line2 = self.x
        line3 = '>'+self.y_description
        line4 = self.y
        return line1 + '\n' + line2 + '\n' + line3 + '\n' + line4

def write_alignment(alignment, file_path):
    with open(file_path, "w") as text_file:
        text_file.write(str(alignment))

