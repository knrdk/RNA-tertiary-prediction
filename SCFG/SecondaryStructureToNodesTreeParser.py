__author__ = 'Konrad Kopciuch'

from Nodes import *


class SecondaryStructureToNodesTreeParser:

    def get_tree(self, secondary_structure, sequence):
        return ROOT(self.__get_tree(secondary_structure, sequence))

    def __get_tree(self, ss, sequence):
        length = len(ss)
        if length == 0:
            return END()
        elif length == 1:
            return MATL(END(), sequence[0])

        first = ss[0]
        last = ss[-1]

        if first == '.':
            child_tree = self.__get_tree(ss[1:], sequence[1:])
            return MATL(child_tree, sequence[0])
        else:
            if last == '.':
                child_tree = self.__get_tree(ss[:-1], sequence[:-1])
                return MATR(child_tree, sequence[-1])
            else:
                if self.__is_first_and_last_basepair(ss):
                    child_tree = self.__get_tree(ss[1:-1], sequence[1:-1])
                    return MATP(child_tree, sequence[0], sequence[-1])
                else:
                    (min_part, max_part) = self.__find_partition(ss)
                    if min_part == max_part:
                        partition_point = min_part + 1
                    elif min_part > (length/2):
                        partition_point = min_part
                    elif max_part < (length/2):
                        partition_point = max_part
                    else:
                        partition_point = int(length/2)
                    left_structure, left_sequence = ss[:partition_point], sequence[:partition_point]
                    right_structure, right_sequence = ss[partition_point:], sequence[partition_point:]
                    left_child = BEGL(self.__get_tree(left_structure, left_sequence))
                    right_child = BEGR(self.__get_tree(right_structure, right_sequence))
                    return BIF(left_child, right_child)

    def __is_first_and_last_basepair(self,ss):
        length = len(ss)
        if length == 0:
            return True

        close_index = self.__get_close_basepair_index(ss, 0)
        return close_index == (length - 1)

    def __find_partition(self, ss):
        assert len(ss)>3 #musza byc conajmniej dwie pary
        first = ss[0]
        assert first == '('

        close_for_first = self.__get_close_basepair_index(ss, 0)
        min = close_for_first + 1
        for i in range(min, len(ss),1):
            if ss[i] == '(':
                return (min,max)
        '''wiadomo ze wyjdziemy w petli for bo jesli funkcja zostala wywolana
        to byla koniecznosc podzialu'''

    @staticmethod
    def __get_close_basepair_index(secondary_structure, open_index):
        assert secondary_structure[open_index] == '('

        length = len(secondary_structure)
        opened = 1
        for index in range(open_index+1, length, 1):
            if secondary_structure[index] == '(':
                opened += 1
            elif secondary_structure[index] == ')':
                opened -= 1

            if opened == 0:
                return index

        raise AttributeError("bledna struktura drugorzedowa")
