__author__ = 'Konrad Kopciuch'

from moderna import load_template


class SequenceProvider:
    '''
    Klasa pelni funkcje proxy dla zapytan o sekwencji pliku PDB,dziki temu ze za kazdym razem nie trzeba parsowac
    tego pliku calosc dziala duzo szybciej.
    '''

    def __init__(self, templates_directory):
        self.templates_directory = templates_directory
        self.sequences = dict()
        self.unmodified = dict()
        self.secondary_structures = dict()

    def get_unmodified_sequence(self, template_file):
        if not self.unmodified.has_key(template_file):
            self.__set_sequence_for_template(template_file)
        return self.unmodified[template_file]

    def get_sequence(self, template_file):
        if not self.sequences.has_key(template_file):
            self.__set_sequence_for_template(template_file)
        return self.sequences[template_file]

    def get_secondary_structure(self, template_file):
        if not self.secondary_structures.has_key(template_file):
            self.__set_sequence_for_template(template_file)
        return self.secondary_structures[template_file]

    def __set_sequence_for_template(self, path):
        full_path = self.templates_directory + path
        tmpl = load_template(full_path)
        seq = tmpl.get_sequence()
        ss = tmpl.get_secstruc()
        self.sequences[path] = str(seq)
        self.unmodified[path] = str(seq.seq_without_modifications)
        self.secondary_structures[path] = str(ss)