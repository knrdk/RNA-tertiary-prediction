__author__ = 'Konrad Kopciuch'

from FamilyFileParser import FamilyFileParser

class CmScanOutputParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_families_above_threshold(self):
        families = list()

        data_in_next_line = False
        with open(self.file_path, 'r') as f:
            for line in f:
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


fam_parser = FamilyFileParser("C:\Users\Konrad\Downloads\\family.txt")
mapping = fam_parser.get_family_name_rfam_id_mapping()

parser = CmScanOutputParser("cmscan_output.txt")
families = parser.get_families_above_threshold()
for (family_name, score) in families:
    rfam_id =  mapping[family_name]
    print rfam_id, family_name, score