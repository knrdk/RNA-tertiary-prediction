__author__ = 'Konrad Kopciuch'


class State(object):

    def __init__(self, value = None):
        self.connected = []
        self.index = None

    def __str__(self):
        return str(self.get_index()) + '\t' + self.__class__.__name__

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def add_connection(self, state):
        self.connected.append(state)

    def get_connected_indexes(self):
        for state in self.connected:
            yield state.get_index()

class S(State):
    pass

class E(State):
    pass

class B(State):
    pass

class MP(State):

    def __init__(self, value):
        self.value = value
        super(MP, self).__init__()

    def __str__(self):
        return str(self.get_index()) + '\t' + self.__class__.__name__ + ' ' + self.value

class ML(State):

    def __init__(self, value):
        self.value = value[0]
        super(ML, self).__init__()

    def __str__(self):
        return str(self.get_index()) + '\t' + self.__class__.__name__ + ' ' + self.value

class MR(State):

    def __init__(self, value):
        self.value = value[-1]
        super(MR, self).__init__()

    def __str__(self):
        return str(self.get_index()) + '\t' + self.__class__.__name__ + ' ' + self.value

class D(State):
    pass

class IL(State):
    def __init__(self):
        super(IL, self).__init__()
        self.add_connection(self)

class IR(State):
    def __init__(self):
        super(IR, self).__init__()
        self.add_connection(self)