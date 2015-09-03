__author__ = 'Konrad Kopciuch'

from States import *

class Node(object):
    split = []
    insert = []

    def __init__(self, child):
        self.child = child
        self.initialize_states()
        self.update_connected()

    def initialize_states(self):
        self.initialize_split_states()
        self.initialize_insert_states()

    def initialize_split_states(self):
        self.split_states = []
        for t in self.__class__.split:
            self.split_states.append(t())

    def initialize_insert_states(self):
        self.insert_states = []
        for t in self.__class__.insert:
            self.insert_states.append(t())

    def update_connected(self):
        for split_state in self.split_states:
            for insert_state in self.insert_states:
                split_state.add_connection(insert_state)
        for state in self.get_self_states():
            for child_split_state in self.get_child_split_states():
                state.add_connection(child_split_state)
        self.connect_IL_to_IR()

    def connect_IL_to_IR(self):
        pass

    def __str__(self):
        self_str = self.__class__.__name__
        child_str = str(self.child)
        return self_str + '\n' + child_str

    def get_number_of_split_states(self):
        return len(self.__class__.split)

    def get_number_of_insert_states(self):
        return len(self.__class__.insert)

    def get_number_of_states(self):
        self_states = self.get_number_of_split_states() + self.get_number_of_insert_states()
        child_states = self.child.get_number_of_states()
        return self_states + child_states

    def get_states(self):
        states = []
        states.extend(self.get_self_states())
        states.extend(self.get_child_states())
        return states

    def get_self_states(self):
        states = []
        states.extend(self.split_states)
        states.extend(self.insert_states)
        return states

    def get_child_states(self):
        return self.child.get_states()

    def get_child_split_states(self):
        return self.child.split_states


class ROOT(Node):
    split = [S]
    insert = [IL, IR]

    def connect_IL_to_IR(self):
        il = self.insert_states[0]
        ir = self.insert_states[1]
        il.add_connection(ir)


class BIF(Node):
    split = [B]

    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.initialize_states()
        self.update_connected()

    def __str__(self):
        self_str = self.__class__.__name__
        left_child_str = str(self.left_child)
        right_child_str = str(self.right_child)
        child_str = left_child_str + '\n' + right_child_str
        return self_str + '\n' + child_str

    def update_connected(self):
        self.split_states[0].add_connection(self.left_child.split_states[0])
        self.split_states[0].add_connection(self.right_child.split_states[0])

    def get_states(self):
        states = []
        states.extend(self.split_states)
        states.extend(self.left_child.get_states())
        states.extend(self.right_child.get_states())
        return states

    def get_number_of_states(self):
        self_states = len(self.__class__.split)
        left_child_states = self.left_child.get_number_of_states()
        right_child_states = self.right_child.get_number_of_states()

        return self_states + left_child_states + right_child_states

class BEGL(Node):
    split = [S]


class BEGR(Node):
    split = [S]
    insert = [IL]

class MATP(Node):
    split = [MP, ML, MR, D]
    insert = [IL, IR]

    def __init__(self, child, nucleotide_1, nucleotide_2):
        self.nucleotide1 = nucleotide_1
        self.nucleotide2 = nucleotide_2
        super(MATP, self).__init__(child)

    def __str__(self):
        self_str = self.__class__.__name__ + ' ' + self.nucleotide1 + self.nucleotide2
        child_str = str(self.child)
        return self_str + '\n' + child_str

    def connect_IL_to_IR(self):
        il = self.insert_states[0]
        ir = self.insert_states[1]
        il.add_connection(ir)

    def initialize_split_states(self):
        value = self.nucleotide1 + self.nucleotide2
        self.split_states = []
        for t in self.__class__.split:
            self.split_states.append(t(value))


class MAT_SingleNode(Node):
    def __init__(self, child, nucleotide):
        self.nucleotide = nucleotide
        super(MAT_SingleNode, self).__init__(child)

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.nucleotide + '\n' + str(self.child)

    def initialize_split_states(self):
        value = self.nucleotide
        self.split_states = []
        for t in self.__class__.split:
            self.split_states.append(t(value))


class MATL(MAT_SingleNode):
    split = [ML, D]
    insert = [IL]


class MATR(MAT_SingleNode):
    split = [MR, D]
    insert = [IR]


class END(Node):
    split = [E]

    def __init__(self):
        self.initialize_states()

    def __str__(self):
        return self.__class__.__name__

    def get_number_of_states(self):
        return len(self.split_states)

    def get_child_states(self):
        return []

    def get_child_split_states(self):
        return []