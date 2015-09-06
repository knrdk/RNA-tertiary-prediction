__author__ = 'Konrad Kopciuch'

from Utils.Alignment import Alignment

class NeedlemanWunsch:
    default_match = 2
    default_mismatch = -3
    default_gap_opening = -5
    default_gap_extending = -2

    def __init__(self, template_sequence, query_sequence):
        '''
        :param template_sequence: Sekwencja szablonu do dopasowania
        :param query_sequence: Sekwencja zapytania do dopasowania
        :return: Zwraca obiekt klasy NeedlemanWunsch za pomoca ktorego mozna dokonac dopasowania sekwencji wejsciowych.
        '''
        self.match = NeedlemanWunsch.default_match
        self.mismatch = NeedlemanWunsch.default_mismatch
        self.gap_opening = NeedlemanWunsch.default_gap_opening
        self.gap_extending = NeedlemanWunsch.default_gap_extending
        self.substitution_matrix = None

        assert isinstance(template_sequence, str)
        assert isinstance(query_sequence, str)

        self.template_sequence = template_sequence
        self.query_sequence = query_sequence
        self.template_length = len(self.template_sequence)
        self.query_length = len(self.query_sequence)
        self.aligned = False
        self.score_for_alignment = 0
        self.alignment = None


    def set_points(self,
                   match=default_match,
                   mismatch=default_mismatch,
                   gap_opening=default_gap_opening,
                   gap_extending=default_gap_extending):
        '''
        Funkcja sluzaca do ustawianie kar wystepujacych w algorytmie NeedlemanaWunscha
        :param match: Punktacja za dopasowanie
        :param mismatch: Kara za brak dopasowania
        :param gap_opening: Kara za otwarcie przerwy
        :param gap_extending: Kara za rozszerzanie przerwy
        :return: Funkcja nic nie zwraca
        '''
        if gap_opening + gap_extending >= mismatch:
            raise ValueError("suma kar gap_opening oraz gap_extending powinna byc mniejsza niz mismatch")
        self.match = match
        self.mismatch = mismatch
        self.gap_opening = gap_opening
        self.gap_extending = gap_extending

    def set_substitution_matrix(self, matrix=None):
        '''
        Funkcja za pomoca mozna ustawic macierz substytucji, gdy taka macierz
        jest ustawiona to zamiast punktacji za dopasowanie/brak dopasowania
        wykorzystywane sa wartosci wystepujace w macierzy.
        Gdy matrix = None to wykorzystywana bedzie standardowa punktacja
        :param matrix: macierz substytucji
        :return:
        '''
        self.substitution_matrix = matrix

    def get_score(self):
        '''
        Funckja zwraca punktacje dla wykonanego dopasowania. Najpierw musi zostac wywolana funkcja align
        :return: Punktacja dla dopasowania
        '''
        if not self.aligned:
            raise RuntimeError("Najpierw nalezy wywolac funkcje align")
        return self.score_for_alignment

    def get_alignment(self):
        '''
        Funkcja zwraca obiekt klasy Alignment zawierajacy dopasowanie sekwencji wejsciowej do sekwencji szablonu.
        Najpierw nalezy wywolac funkcje align
        :return: Dopasowanie sekwencji
        '''
        if not self.aligned:
            raise RuntimeError("Najpierw nalazy wywolac funkcja align")
        if self.alignment == None:
            self.__find_alignment()
        return self.alignment

    def align(self):
        '''
        Funckja wykonuje algorytm Needlemana-Wunscha dla zadanych sekwencji.
        :return:
        '''
        self.__create_matrices()
        self.__initialize_matrices()

        for i in range(1, self.query_length+1, 1):
            for j in range(1, self.template_length+1, 1):
                self.__calculate_value_for_IX_matrix(i, j)
                self.__calculate_value_for_IY_matrix(i, j)
                self.__calculate_value_for_M_matrix(i, j)

        self.score_for_alignment = self.M_matrix[self.query_length][self.template_length][0]
        self.aligned = True

    def __find_alignment(self):
        '''
        Funckja znajduje dopasowanie sekwencji na podstawie wczesniej wykonanego algorytmu Needlemana-Wunscha
        :return:
        '''
        #j - pozycja w template_sequence
        #i - pozycja w query_sequence
        template_alignment, query_alignment = '', ''
        current_matrix = 'M'
        i, j = self.query_length, self.template_length
        previous_matrix = self.M_matrix[i][j][1]
        while not (i==0 and j==0):
            if current_matrix == 'M':
                if previous_matrix == 'M':
                    template_alignment = self.template_sequence[j-1] + template_alignment
                    query_alignment = self.query_sequence[i-1] + query_alignment
                    i,j = i-1, j-1
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'X':
                    current_matrix = 'X'
                    previous_matrix = self.IX_matrix[i][j][1]
                else:
                    current_matrix = 'Y'
                    previous_matrix = self.IY_matrix[i][j][1]
            elif current_matrix == 'X':
                template_alignment = '-' + template_alignment
                query_alignment = self.query_sequence[i-1] + query_alignment
                i,j = i-1,j
                if previous_matrix == 'M':
                    current_matrix = 'M'
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'X':
                    previous_matrix = self.IX_matrix[i][j][1]
                else:
                    j-=1
            else:
                template_alignment = self.template_sequence[j-1] + template_alignment
                query_alignment = '-' + query_alignment
                i,j = i,j-1
                if previous_matrix == 'M':
                    current_matrix = 'M'
                    previous_matrix = self.M_matrix[i][j][1]
                elif previous_matrix == 'Y':
                    previous_matrix = self.IY_matrix[i][j][1]
                else:
                    i-=1
        self.alignment = Alignment(template_alignment, query_alignment)


    def __calculate_value_for_M_matrix(self, i, j):
        points_for_match = self.__get_points_for_match(self.template_sequence[j-1], self.query_sequence[i-1])

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
        width = 1 + self.template_length
        height = 1 + self.query_length
        self.M_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IX_matrix = [[0 for x in range(width)] for x in range(height)]
        self.IY_matrix = [[0 for x in range(width)] for x in range(height)]

    def __initialize_matrices(self):
        self.__initialize_M_matrix()
        self.__initialize_IX_matrix()
        self.__initialize_IY_matrix()

    def __initialize_M_matrix(self):
        self.M_matrix[0][0] = (0, None)
        for i in range(self.template_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[0][1+i] = (value, 'Y')
        for i in range(self.query_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.M_matrix[1+i][0] = (value, 'X')

    def __initialize_IX_matrix(self):
        minus_inf = -float("inf")
        for i in range(self.template_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IX_matrix[0][1+i] = (value, 'X')
        for i in range(0, self.query_length+1, 1):
            self.IX_matrix[i][0] = (minus_inf, 'X')

    def __initialize_IY_matrix(self):
        minus_inf = -float("inf")
        for i in range(0, self.template_length+1, 1):
            self.IY_matrix[0][i] = (minus_inf, 'Y')
        for i in range(self.query_length):
            value = self.gap_opening + (i+1)*self.gap_extending
            self.IY_matrix[1+i][0] = (value, 'Y')

    def __get_points_for_match(self, a, b):
        if self.substitution_matrix == None:
            if a == b:
                return self.match
            else:
                return self.mismatch
        else:
            try: #macierz substytucji jest dolno/gorno trojkatna
                return self.substitution_matrix[a][b]
            except:
                return self.substitution_matrix[b][a]
