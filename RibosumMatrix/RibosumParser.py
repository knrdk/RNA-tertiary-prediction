__author__ = 'Konrad Kopciuch'

class RibosumParser:
    letters = ['A','C','G','U']

    def __init__(self, path):
        self.path = path
        self.single_matrix_lines = None
        self.double_matrix_lines = None

    def get_single_matrix(self):
        if not self.single_matrix_lines:
            self.__read_file()
        return RibosumParser.__get_matrix(RibosumParser.letters, self.single_matrix_lines)

    def get_double_matrix(self):
        if not self.double_matrix_lines:
            self.__read_file()
        double_letters = list(RibosumParser.__get_double_letters())
        return RibosumParser.__get_matrix(double_letters, self.double_matrix_lines)

    def __read_file(self):
        with open(self.path,'U') as f:
            lines = list(f)
            self.single_matrix_lines = lines[3:7]
            self.double_matrix_lines = lines[11:27]

    @staticmethod
    def __get_matrix(labels, lines):
        scores = RibosumParser.__get_scores(lines)
        matrix = RibosumParser.__get_2d_dictionary(labels)
        for i in range(len(labels)):
            for j in range(i+1):
                matrix[labels[i]][labels[j]] = scores.pop(0)
        return matrix

    @staticmethod
    def __get_2d_dictionary(keys):
        matrix = {}
        for l in keys:
            matrix[l] = {}
        return matrix

    @staticmethod
    def __get_scores(lines):
        scores = []
        for line in lines:
            values = line.split(' ')
            for value in filter(lambda x: x and x!='\n', values)[1:]:
                scores.append(float(value))
        return scores

    @staticmethod
    def __get_double_letters():
        for x in RibosumParser.letters:
            for y in RibosumParser.letters:
                yield x + y