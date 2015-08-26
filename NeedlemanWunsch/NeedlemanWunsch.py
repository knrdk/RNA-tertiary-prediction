__author__ = 'Konrad Kopciuch'

from Alignment import Alingment

class NeedlemanWunsch:
    default_match = 2
    default_mismatch = -3
    default_gap_opening = -5
    default_gap_extending = -2

    def __init__(self, query_sequence, subject_sequence):
        self.match = NeedlemanWunsch.default_match
        self.mismatch = NeedlemanWunsch.default_mismatch
        self.gap_opening = NeedlemanWunsch.default_gap_opening
        self.gap_extending = NeedlemanWunsch.default_gap_extending

        assert isinstance(query_sequence, str)
        assert isinstance(subject_sequence, str)
        self.x_sequence = query_sequence
        self.y_sequence = subject_sequence
        self.x_length = len(self.x_sequence)
        self.y_length = len(self.y_sequence)
        self.aligned = False
        self.score_for_alignment = 0
        self.alignment = None

    def set_points(self,
                   match=default_match,
                   mismatch=default_mismatch,
                   gap_opening=default_gap_opening,
                   gap_extending=default_gap_extending):
        if gap_opening + gap_extending >= mismatch:
            raise ValueError("gap_opening + gap_extending should be less then mismatch value")
        self.match = match
        self.mismatch = mismatch
        self.gap_opening = gap_opening
        self.gap_extending = gap_extending

    def get_score(self):
        if not self.aligned:
            raise RuntimeError("You must call 'align' first")
        return self.score_for_alignment

    def get_alignment(self):
        if not self.aligned:
            raise RuntimeError("You must call 'align' first")
        if self.alignment == None:
            self.__find_alignment()
        return self.alignment

    def align(self):
        self.__create_matrices()
        self.__initialize_matrices()

        for i in range(1,self.y_length+1,1):
            for j in range(1, self.x_length+1,1):
                self.__calculate_value_for_IX_matrix(i, j)
                self.__calculate_value_for_IY_matrix(i, j)
                self.__calculate_value_for_M_matrix(i, j)

        self.score_for_alignment = self.M_matrix[self.y_length][self.x_length].value
        self.aligned = True

    def __find_alignment(self):
        assert self.aligned

        start =  self.M_matrix[self.y_length][self.x_length]# MatrixElement(None, self.M_matrix, self.y_length, self.x_length)
        (query_align, subject_align) = self.__find_alignment_private(self.x_sequence, self.y_sequence, start, self.M_matrix)
        self.alignment = Alingment(query_align, subject_align)

    def __find_alignment_private(self, subject, query, current, current_matrix):
        if current is None:
            return ("", "")

        if len(query) == 0 or len(subject) == 0:
            return ("","")

        previous = current.previous_matrix[current.previous_i][current.previous_j]
        if current.previous_matrix == self.M_matrix:
            pass
        if current_matrix == self.M_matrix:
            if current.previous_matrix == self.IX_matrix or current.previous_matrix == self.IY_matrix:
                return self.__find_alignment_private(subject, query, previous, current.previous_matrix)

        if current.previous_matrix == self.M_matrix:
            subject_last = subject[-1]
            query_last = query[-1]
            (subject_alignment, query_alignment) = self.__find_alignment_private(subject[:-1], query[:-1], previous, current.previous_matrix)
            return (subject_alignment + subject_last, query_alignment + query_last)
        elif current.previous_matrix == self.IX_matrix:
            query_last = query[-1]
            (subject_alignment, query_alignment) = self.__find_alignment_private(subject, query[:-1], previous, current.previous_matrix)
            return (subject + '-', query_alignment + query_last)
        else:
            subject_last = subject[-1]
            (subject_alignment, query_alignment) = self.__find_alignment_private(subject[:-1], query, previous, current.previous_matrix)
            return (subject_alignment + subject_last, query_alignment + '-')


    def __calculate_value_for_M_matrix(self, i, j):
        points_for_match = self.__get_points_for_match(self.x_sequence[j-1], self.y_sequence[i-1])

        match_score = self.M_matrix[i-1][j-1].value + points_for_match
        ix_gap_score = self.IX_matrix[i][j].value
        iy_gap_score = self.IY_matrix[i][j].value

        if match_score > max(ix_gap_score, iy_gap_score):
            self.M_matrix[i][j] = MatrixElement(match_score, self.M_matrix, i-1, j-1)
        elif ix_gap_score > iy_gap_score:
            self.M_matrix[i][j] = MatrixElement(ix_gap_score, self.IX_matrix, i, j)
        else:
            self.M_matrix[i][j] = MatrixElement(iy_gap_score, self.IY_matrix, i, j)

    def __calculate_value_for_IX_matrix(self, i, j):
        open_score = self.M_matrix[i-1][j].value + self.gap_opening + self.gap_extending
        extend_score = self.IX_matrix[i-1][j].value + self.gap_extending

        if open_score > extend_score:
            self.IX_matrix[i][j] = MatrixElement(open_score, self.M_matrix, i-1, j)
        else:
            self.IX_matrix[i][j] = MatrixElement(extend_score, self.IX_matrix, i-1, j)

    def __calculate_value_for_IY_matrix(self, i, j):
        open_score = self.M_matrix[i][j-1].value + self.gap_opening + self.gap_extending
        extend_score = self.IY_matrix[i][j-1].value + self.gap_extending

        if open_score > extend_score:
            self.IY_matrix[i][j] = MatrixElement(open_score, self.M_matrix, i, j-1)
        else:
            self.IY_matrix[i][j] = MatrixElement(extend_score, self.IY_matrix, i, j-1)

    def __create_matrices(self):
        width = 1 + self.x_length
        height = 1 + self.y_length
        self.M_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IX_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IY_matrix = [[0 for x in range(width)] for x in range(height)]

    def __initialize_matrices(self):
        self.__initialize_M_matrix()
        self.__initialize_IX_matrix()
        self.__initialize_IY_matrix()

    def __initialize_M_matrix(self):
        self.M_matrix[0][0] = MatrixElement(0)
        for i in range(self.x_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[0][1+i] = MatrixElement(value, self.M_matrix, 0, i)
        for i in range(self.y_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[1+i][0] = MatrixElement(value, self.M_matrix, i, 0)

    def __initialize_IX_matrix(self):
        minus_inf = -float("inf")
        self.IX_matrix[0][0] = MatrixElement(minus_inf)
        for i in range(self.x_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IX_matrix[0][1+i] = MatrixElement(value, self.IX_matrix, 0, i)
        for i in range(self.y_length):
            self.IX_matrix[1+i][0] = MatrixElement(minus_inf)

    def __initialize_IY_matrix(self):
        minus_inf = -float("inf")
        self.IY_matrix[0][0] = MatrixElement(minus_inf)
        for i in range(self.x_length):
            self.IY_matrix[0][1+i] = MatrixElement(minus_inf)
        for i in range(self.y_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IY_matrix[1+i][0] = MatrixElement(value, self.IY_matrix, i, 0)

    def __get_points_for_match(self, a, b):
        if a == b:
            return self.match
        else:
            return self.mismatch

class MatrixElement:
    def __init__(self, value, previous_matrix = None, previous_i = None, previous_j = None):
        self.value = value
        self.previous_matrix = previous_matrix
        self.previous_i = previous_i
        self.previous_j = previous_j
