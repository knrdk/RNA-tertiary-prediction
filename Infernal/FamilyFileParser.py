__author__ = 'Konrad Kopciuch'

class FamilyFileParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_family_name_rfam_id_mapping(self):
        mapping = dict()
        with open(self.file_path, 'r') as file:
            for line in file:
                splitted_line = line.split('\t')
                rfam_id, family_name = splitted_line[0], splitted_line[1]
                mapping[family_name] = rfam_id
        return mapping