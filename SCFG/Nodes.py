__author__ = 'Konrad Kopciuch'

from States import *

class Node(object):
    split_states = []
    insert_states = []

    def __init__(self, child):
        self.child = child

    def __str__(self):
        self_str = self.__class__.__name__
        child_str = str(self.child)
        return self_str + '\n' + child_str

    def get_number_of_split_states(self):
        return len(self.__class__.split_states)

    def get_number_of_insert_states(self):
        return len(self.__class__.insert_states)

    def get_number_of_states(self):
        self_states = self.get_number_of_split_states() + self.get_number_of_insert_states()
        child_states = self.child.get_number_of_states()
        return self_states + child_states

class ROOT(Node):
    split_states = [S]
    insert_states = [IL, IR]


class BIF(Node):
    split_states = [B]

    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        self_str = self.__class__.__name__
        left_child_str = str(self.left_child)
        right_child_str = str(self.right_child)
        child_str = left_child_str + '\n' + right_child_str
        return self_str + '\n' + child_str

    def get_number_of_states(self):
        self_states = len(self.split_states)
        left_child_states = self.left_child.get_number_of_states()
        right_child_states = self.right_child.get_number_of_states()

        return self_states + left_child_states + right_child_states

class BEGL(Node):
    split_states = [S]


class BEGR(Node):
    split_states = [S]
    insert_states = [IL]


class MATP(Node):
    split_states = [MP, ML, MR, D]
    insert_states = [IL, IR]

    def __init__(self, child, nucleotide_1, nucleotide_2):
        super(MATP, self).__init__(child)
        self.nucleotiede_1 = nucleotide_1
        self.nucleotiede_2 = nucleotide_2

    def __str__(self):
        self_str = self.__class__.__name__ + ' ' + self.nucleotiede_1 + self.nucleotiede_2
        child_str = str(self.child)
        return self_str + '\n' + child_str


class MAT_SingleNode(Node):
    def __init__(self, child, nucleotide):
        super(MAT_SingleNode, self).__init__(child)
        self.nucleotide = nucleotide

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.nucleotide + '\n' + str(self.child)


class MATL(MAT_SingleNode):
    split_states = [ML, D]
    insert_states = [IL]


class MATR(MAT_SingleNode):
    split_states = [MR, D]
    insert_states = [IR]


class END(Node):
    split_states = [E]

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def get_number_of_states(self):
        return len(self.split_states)