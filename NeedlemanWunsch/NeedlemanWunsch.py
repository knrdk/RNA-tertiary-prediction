__author__ = 'Konrad Kopciuch'

from Utils.Alignment import Alignment

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
        self.substitution_matrix = None

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

    def set_substitution_matrix(self, matrix):
        self.substitution_matrix = matrix

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

        for i in range(1, self.y_length+1, 1):
            for j in range(1, self.x_length+1, 1):
                self.__calculate_value_for_IX_matrix(i, j)
                self.__calculate_value_for_IY_matrix(i, j)
                self.__calculate_value_for_M_matrix(i, j)

        self.score_for_alignment = self.M_matrix[self.y_length][self.x_length][0]
        self.aligned = True

    def __find_alignment(self):
        #j - pozycja w sequence_x
        #i - pozycja w sequence_y
        algn_x, algn_y = '', ''
        current_matrix = 'M'
        i, j = self.y_length, self.x_length
        previous_matrix = self.M_matrix[i][j][1]
        while not (i==0 and j==0):
            if current_matrix == 'M':
                if previous_matrix == 'M':
                    algn_x = self.x_sequence[j-1] + algn_x
                    algn_y = self.y_sequence[i-1] + algn_y
                    i,j = i-1, j-1
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'X':
                    current_matrix = 'X'
                    previous_matrix = self.IX_matrix[i][j][1]
                else:
                    current_matrix = 'Y'
                    previous_matrix = self.IY_matrix[i][j][1]
            elif current_matrix == 'X':
                algn_x = '-' + algn_x
                algn_y = self.y_sequence[i-1] + algn_y
                i,j = i-1,j
                if previous_matrix == 'M':
                    current_matrix = 'M'
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'X':
                    previous_matrix = self.IX_matrix[i][j][1]
                else:
                    j-=1
            else:
                algn_x = self.x_sequence[j-1] + algn_x
                algn_y = '-' + algn_y
                i,j = i,j-1
                if previous_matrix == 'M':
                    current_matrix = 'M'
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'Y':
                    previous_matrix = self.IY_matrix[i][j][1]
                else:
                    i-=1
        self.alignment = Alignment(algn_x, algn_y)


    def __calculate_value_for_M_matrix(self, i, j):
        points_for_match = self.__get_points_for_match(self.x_sequence[j-1], self.y_sequence[i-1])

        match_score = self.M_matrix[i-1][j-1][0] + points_for_match
        ix_gap_score = self.IX_matrix[i][j][0]
        iy_gap_score = self.IY_matrix[i][j][0]

        if match_score > max(ix_gap_score, iy_gap_score):
            self.M_matrix[i][j] = (match_score, 'M')
        elif ix_gap_score > iy_gap_score:
            self.M_matrix[i][j] = (ix_gap_score, 'X')
        else:
            self.M_matrix[i][j] = (iy_gap_score, 'Y')

    def __calculate_value_for_IX_matrix(self, i, j):
        open_score = self.M_matrix[i-1][j][0] + self.gap_opening + self.gap_extending
        extend_score = self.IX_matrix[i-1][j][0] + self.gap_extending

        if open_score > extend_score:
            self.IX_matrix[i][j] = (open_score, 'M')
        else:
            self.IX_matrix[i][j] = (extend_score, 'X')

    def __calculate_value_for_IY_matrix(self, i, j):
        open_score = self.M_matrix[i][j-1][0] + self.gap_opening + self.gap_extending
        extend_score = self.IY_matrix[i][j-1][0] + self.gap_extending

        if open_score > extend_score:
            self.IY_matrix[i][j] = (open_score, 'M')
        else:
            self.IY_matrix[i][j] = (extend_score, 'Y')

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
        self.M_matrix[0][0] = (0, None)
        for i in range(self.x_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[0][1+i] = (value, 'Y')
        for i in range(self.y_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[1+i][0] = (value, 'X')

    def __initialize_IX_matrix(self):
        minus_inf = -float("inf")
        for i in range(self.x_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IX_matrix[0][1+i] = (value, 'X')
        for i in range(0, self.y_length+1, 1):
            self.IX_matrix[i][0] = (minus_inf, 'X')

    def __initialize_IY_matrix(self):
        minus_inf = -float("inf")
        for i in range(0, self.x_length+1, 1):
            self.IY_matrix[0][i] = (minus_inf, 'Y')
        for i in range(self.y_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IY_matrix[1+i][0] = (value, 'Y')

    def __get_points_for_match(self, a, b):
        if self.substitution_matrix == None:
            if a == b:
                return self.match
            else:
                return self.mismatch
        else:
            try:
                return self.substitution_matrix[a][b]
            except:
                try:
                    return self.substitution_matrix[b][a]
                except:
                    return self.mismatch
