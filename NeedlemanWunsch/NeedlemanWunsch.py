__author__ = 'Konrad Kopciuch'

class Directions:
    Left = 1
    Right = 2
    Up = 4
    Down = 8

class States:
    M = 1 #Mathc
    IX = 2 #x aligned to gap
    IY = 4 #y aligned to gap

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
        self.score_for_alignment = None
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
        if None == self.score_for_alignment:
            raise RuntimeError("You must call 'align' first")
        return self.score_for_alignment

    def align(self):
        self.__create_matrices()
        self.__initialize_matrices()

        for i in range(1,self.y_length+1,1):
            for j in range(1, self.x_length+1,1):
                self.__calculate_value_for_M_matrix(i, j)
                self.__calculate_value_for_IX_matrix(i, j)
                self.__calculate_value_for_IY_matrix(i, j)

        self.score_for_alignment = self.M_matrix[self.y_length][self.x_length]

    def __calculate_value_for_M_matrix(self, i, j):
        points_for_match = self.__get_points_for_match(self.x_sequence[j-1], self.y_sequence[i-1])
        match_score = self.M_matrix[i-1][j-1] + points_for_match
        ix_gap_score = self.IX_matrix[i-1][j-1] + points_for_match
        iy_gap_score = self.IY_matrix[i-1][j-1] + points_for_match
        max_score = max(match_score, ix_gap_score, iy_gap_score)

        try:
            self.M_matrix[i][j] = max_score
        except:
            print i,j

    def __calculate_value_for_IX_matrix(self, i, j):
        open_score = self.M_matrix[i-1][j] + self.gap_opening
        extend_score = self.IX_matrix[i-1][j] + self.gap_extending
        max_score = max(open_score, extend_score)

        self.IX_matrix[i][j] = max_score

    def __calculate_value_for_IY_matrix(self, i, j):
        open_score = self.M_matrix[i][j-1] + self.gap_opening
        extend_score = self.IY_matrix[i][j-1] + self.gap_extending
        max_score = max(open_score, extend_score)

        self.IY_matrix[i][j] = max_score

    def __create_matrices(self):
        width = 1 + self.x_length
        height = 1 + self.y_length
        self.M_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IX_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IY_matrix = [[0 for x in range(width)] for x in range(height)]
        self.directions_matrix = [[0 for x in range(width)] for x in range(height)]

    def __initialize_matrices(self):
        self.__initialize_M_matrix()
        self.__initialize_IX_matrix()
        self.__initialize_IY_matrix()

    def __initialize_M_matrix(self):
        self.M_matrix[0][0] = 0
        for i in range(self.x_length):
            self.M_matrix[0][1+i] = self.gap_opening + (i+1)*self.gap_extending
        for i in range(self.y_length):
            self.M_matrix[1+i][0] = self.gap_opening + (i+1)*self.gap_extending

    def __initialize_IX_matrix(self):
        minus_inf = -float("inf")
        self.IX_matrix[0][0] = minus_inf
        for i in range(self.x_length):
            self.IX_matrix[0][1+i] = self.gap_opening + (i+1)*self.gap_extending
        for i in range(self.y_length):
            self.IX_matrix[1+i][0] = minus_inf

    def __initialize_IY_matrix(self):
        minus_inf = -float("inf")
        self.IY_matrix[0][0] = minus_inf
        for i in range(self.x_length):
            self.IY_matrix[0][1+i] = minus_inf
        for i in range(self.y_length):
            self.IY_matrix[1+i][0] = self.gap_opening + (i+1)*self.gap_extending

    def __get_points_for_match(self, a, b):
        if a==b:
            return self.match
        else:
            return self.mismatch
