__author__ = 'Konrad Kopciuch'

class CmScanOutputParser:

    def __init__(self, output):
        self.output = output

    def get_families_above_threshold(self):
        '''
        Funkcja zwraca rodziny z bazy RFAM do ktorych moze nalezec dana sekwencja
        :return: lista dwojek: family_name, score
        '''
        families = list()

        data_in_next_line = False
        for line in self.output.split('\n'):
            if data_in_next_line:
                if len(line) == 0 or line[1:3] == "--":
                    return families
                x = self.__parse_line(line)
                families.append(x)
            else:
                data_in_next_line = (line[1:3] == "--")
        return families

    def __parse_line(self, line):
        splitted = line.split(' ')
        removed_empty_strings = [x for x in splitted if len(x)>0]
        score = float(removed_empty_strings[3])/100
        family_name = removed_empty_strings[5]
        return family_name, score