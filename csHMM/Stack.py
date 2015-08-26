__author__ = 'Konrad Kopciuch'

class Stack:
    def __init__(self):
        self.__stack = []

    def is_empty(self):
        length = len(self.__stack)
        return 0 == length

    def push(self, value):
        self.__stack.append(value)

    def pop(self):
        return self.__stack.pop()
