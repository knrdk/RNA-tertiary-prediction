__author__ = 'Konrad Kopciuch'

class RibosumParser:
    '''
    Klasa sluzy do parsowania pliku zawierajacego macierze Ribosum
    '''
    letters = ['A', 'C', 'G', 'U']

    def __init__(self, path):
        '''
        Konstruktor przyjmuje sciezke do pliku macierzy
        :param path: Sciezka do pliku z macierza Ribosum
        :return: Obiekt klasy RibosumParser
        '''
        self.path = path
        self.single_matrix_lines = None
        self.double_matrix_lines = None

    def get_single_matrix(self):
        '''
        :return: Slownik zawierajacy punktacje dopasowan pojedynczych nukelotydow
        '''
        if not self.single_matrix_lines:
            self.__read_file()
        return RibosumParser.__get_matrix(RibosumParser.letters, self.single_matrix_lines)

    def get_double_matrix(self):
        '''
        :return: Slownik zawierajacy punktacje dopasowac par nukleotydow
        '''
        if not self.double_matrix_lines:
            self.__read_file()
        double_letters = list(RibosumParser.__get_double_letters())
        return RibosumParser.__get_matrix(double_letters, self.double_matrix_lines)

    def __read_file(self):
        '''
        Funkcja czyta plik z macierzami Ribosum i zapisuje do zmiennych linie zawierajace macierze
        :return:
        '''
        with open(self.path,'U') as f:
            lines = list(f)
            self.single_matrix_lines = lines[3:7] #linie z pojedyncza macierza
            self.double_matrix_lines = lines[11:27] #linie z podwojna macierza

    @staticmethod
    def __get_matrix(labels, lines):
        '''
        Funkcja czyta z przekazanych linii pliku punktacje dopasowan i zapisuje je w slowniku
        Etykiety posortowane sa alfabetycznie
        :param labels: Etykiety, w tym przypadku albo pojedyncze nukelotydy, albo pary
        :param lines: linie w ktorych jest macierz
        :return:
        '''
        scores = RibosumParser.__get_scores(lines)
        matrix = RibosumParser.__get_2d_dictionary(labels)
        for i in range(len(labels)):
            for j in range(i+1):
                matrix[labels[i]][labels[j]] = scores.pop(0)
        return matrix

    @staticmethod
    def __get_2d_dictionary(keys):
        '''
        zwraca slownik dwuwymiarowy o odpowiednich kluczach
        :param keys: klucze slownika
        :return: dwuwymiarowy slownik
        '''
        matrix = {}
        for l in keys:
            matrix[l] = {}
        return matrix

    @staticmethod
    def __get_scores(lines):
        '''
        Funkcja czyta z podanych linii punktacje i zwraca jednowymiarowa liste tych punktacji
        :param lines: liniie zawierajace macierz ribosum
        :return: lista punktacji
        '''
        scores = []
        for line in lines:
            values = line.split(' ')
            for value in filter(lambda x: x and x!='\n', values)[1:]:
                scores.append(float(value))
        return scores

    @staticmethod
    def __get_double_letters():
        '''
        Funkcja wylicza pary nukleotydow
        :return: Lista 16 par: AA, AC, AG, ... UU
        '''
        for x in RibosumParser.letters:
            for y in RibosumParser.letters:
                yield x + y