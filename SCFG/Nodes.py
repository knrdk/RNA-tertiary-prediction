__author__ = 'Konrad Kopciuch'

from States import *

class Node(object):
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return self.__class__.__name__ + '\n' + str(self.child)


class ROOT(Node):

    def __init__(self, child):
        super(ROOT, self).__init__(child)
        #self.split_states = [S]
        #self.insert_states = [IL, IR]

class BIF:
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return self.__class__.__name__ + '\n' + str(self.left_child) + '\n' + str(self.right_child)


class BEGL(Node):
    pass


class BEGR(Node):
    pass


class MATP(Node):
    def __init__(self, child, nucleotide_1, nucleotide_2):
        super(MATP, self).__init__(child)
        self.nucleotiede_1 = nucleotide_1
        self.nucleotiede_2 = nucleotide_2

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.nucleotiede_1 + self.nucleotiede_2 + '\n' + str(self.child)


class MATL(Node):
    def __init__(self, child, nucleotide):
        super(MATL, self).__init__(child)
        self.nucleotide = nucleotide

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.nucleotide + '\n' + str(self.child)

class MATR(Node):
    def __init__(self, child, nucleotide):
        super(MATR, self).__init__(child)
        self.nucleotide = nucleotide

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.nucleotide + '\n' + str(self.child)

class END:
    def __str__(self):
        return self.__class__.__name__
