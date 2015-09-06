__author__ = 'Konrad Kopciuch'


class Alignment:
    def __init__(self, template_sequence, query_sequence):
        assert len(template_sequence) == len(query_sequence)

        self.template = template_sequence
        self.query = query_sequence
        self.length = len(self.template)
        self.template_description = ''
        self.query_description = ''

    def get_identity_percent(self):
        if self.length == 0:
            return 1
        identical = 0.0
        for i in range(self.length):
            if self.template[i] == self.query[i]:
                identical+=1
        return identical/self.length

    def set_template_description(self, description):
        self.template_description = description

    def set_query_description(self, description):
        self.query_description = description

    def __get_length_without_gap(self, sequence):
        i=0
        for c in sequence:
            if c != '-':
                i+=1
        return i

    def get_template_sequence(self):
        z = ''
        for c in self.template:
            if c != '-':
                z = z + c
        return z

    def get_query_sequence(self):
        z = ''
        for c in self.query:
            if c != '-':
                z = z + c
        return z

    def change_template_sequence(self, new_sequence):
        assert len(new_sequence) == self.__get_length_without_gap(self.template)
        z = ''
        i = 0
        for c in self.template:
            if c == '-':
                z = z + '-'
            else:
                z = z + new_sequence[i]
                i+=1
        self.template = z

    def change_query_sequence(self, new_sequence):
        assert len(new_sequence) == self.__get_length_without_gap(self.query)
        z = ''
        i = 0
        for c in self.query:
            if c == '-':
                z = z + '-'
            else:
                z = z + new_sequence[i]
                i+=1
        self.query = z

    def __str__(self):
        line1 = '>'+self.template_description
        line2 = self.template
        line3 = '>'+self.query_description
        line4 = self.query
        return line1 + '\n' + line2 + '\n' + line3 + '\n' + line4

def write_alignment(alignment, file_path):
    with open(file_path, "w") as text_file:
        text_file.write(str(alignment))

