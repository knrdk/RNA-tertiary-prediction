__author__ = 'Konrad Kopciuch'

class CmScanOutputParser:

    def __init__(self, output):
        self.output = output

    def get_families_above_threshold(self):
        families = list()

        data_in_next_line = False
        for line in self.output.split('\n'):
            if data_in_next_line:
                if line[1:3] == "--":
                    return families
                x = self.__parse_line(line)
                families.append(x)
            else:
                data_in_next_line = (line[1:3] == "--")

    def __parse_line(self, line):
        splitted = line.split(' ')
        removed_empty_strings = [x for x in splitted if len(x)>0]
        score = removed_empty_strings[3]
        family_name = removed_empty_strings[5]
        return family_name, score