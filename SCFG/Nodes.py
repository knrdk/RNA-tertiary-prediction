__author__ = 'Konrad Kopciuch'

class Node:
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return self.__class__.__name__ + '\n' + str(self.child)


class ROOT(Node):
    pass

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
    pass

class MATL(Node):
    pass

class MATR(Node):
    pass

class END:
    def __str__(self):
        return self.__class__.__name__
