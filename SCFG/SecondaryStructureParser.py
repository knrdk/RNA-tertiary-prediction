__author__ = 'Konrad Kopciuch'

from Nodes import *


class SecondaryStructureParser:

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
                    if min_part > (length/2):
                        partition_point = min_part
                    elif max_part < (length/2):
                        partition_point = max_part
                    else:
                        partition_point = int(length/2)
                    left_child = BEGL(self.__get_tree(ss[:partition_point], sequence[:partition_point]))
                    right_child = BEGR(self.__get_tree(ss[partition_point:], sequence[partition_point:]))
                    return BIF(left_child, right_child)

    def __is_first_and_last_basepair(self,ss):
        length = len(ss)
        if length == 0:
            return True

        first = ss[0]
        last = ss[-1]
        if first == '.':
            if last == '.':
                return self.__is_first_and_last_basepair(ss[1:-1])
            else:
                return self.__is_first_and_last_basepair(ss[1:])
        elif last == '.':
            return self.__is_first_and_last_basepair(ss[:-1])
        elif first== '(' and last == ')':
            return self.__is_first_and_last_basepair(ss[1:-1])
        else:
            return False


    def __find_partition(self, ss):
        assert len(ss)>3 #musza byc conajmniej dwie pary
        first = ss[0]
        assert first == '('

        number_of_opened_braces = 1
        min_point = 0
        for i in range(1,len(ss),1):
            if ss[i]=='(':
                number_of_opened_braces+=1
            elif ss[i]==')':
                number_of_opened_braces-=1

            if min_point==0 and number_of_opened_braces==0:
                min_point = i

            if min_point!=0 and number_of_opened_braces!=0:
                return (min_point, i-1)

            elif min_point!=0 and i==len(ss)-1:
                return (min_point, i)
