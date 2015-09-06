__author__ = 'Konrad Kopciuch'


class StateTypes:
    P, L, R, B, D, S, E = range(7)


class State(object):

    def __init__(self, value = None):
        self.connected = []
        self.index = None

    def __str__(self):
        return self.__class__.__name__

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def set_gap_class(self, gap_class):
        self.gap_class = gap_class

    def get_gap_class(self):
        return self.gap_class

    def add_connection(self, state):
        self.connected.append(state)

    def get_connected_indexes(self):
        for state in self.connected:
            yield state.get_index()


class S(State):
    state_type = StateTypes.S


class E(State):
    state_type = StateTypes.E


class B(State):
    state_type = StateTypes.B


class MP(State):
    state_type = StateTypes.P

    def __init__(self, value):
        self.value = value
        super(MP, self).__init__()

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.value


class ML(State):
    state_type = StateTypes.L

    def __init__(self, value):
        self.value = value[0]
        super(ML, self).__init__()

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.value


class MR(State):
    state_type = StateTypes.R

    def __init__(self, value):
        self.value = value[-1]
        super(MR, self).__init__()

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.value


class D(State):
    state_type = StateTypes.D


class IL(State):
    state_type = StateTypes.L

    def __init__(self):
        super(IL, self).__init__()
        self.add_connection(self)
        self.value = None


class IR(State):
    state_type = StateTypes.R

    def __init__(self):
        super(IR, self).__init__()
        self.add_connection(self)
        self.value = None