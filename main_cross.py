__author__ = 'rna'

from Config import Config
from os import listdir
from moderna import load_template, load_alignment, create_model, clean_structure
from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from NeedlemanWunsch.Alignment import *
from RMSD.RMSD import get_rmsd


class SequenceProvider:

    def __init__(self, templates_directory):
        self.templates_directory = templates_directory
        self.sequences = dict()
        self.unmodified = dict()

    def get_unmodified_sequence(self, template_file):
        if not self.unmodified.has_key(template_file):
            self.__set_sequence_for_template(template_file)
        return self.unmodified[template_file]

    def get_sequence(self, template_file):
        if not self.sequences.has_key(template_file):
            self.__set_sequence_for_template(template_file)
        return self.sequences[template_file]

    def __set_sequence_for_template(self, path):
        full_path = self.templates_directory + path
        tmpl = load_template(full_path)
        seq = tmpl.get_sequence()
        self.sequences[path] = str(seq)
        self.unmodified[path] = str(seq.seq_without_modifications)


def main():
    cfg = Config('config.ini')
    templates_directory = cfg.get_template_directory()
    sp = SequenceProvider(templates_directory)

    templates_paths = list(listdir(templates_directory))
    i = 1
    for query_path in templates_paths:
        rmsds = []
        for template_path in templates_paths:
            if query_path == template_path:
                continue
            print i
            print query_path, template_path
            query_sequence = sp.get_sequence(query_path)
            query_sequence_without_modifications = sp.get_unmodified_sequence(query_path)
            template_sequence = sp.get_sequence(template_path)
            template_sequence_without_modifications = sp.get_unmodified_sequence(template_path)
            nw = NeedlemanWunsch(query_sequence_without_modifications,template_sequence_without_modifications)
            nw.align()
            algn = nw.get_alignment()
            algn.change_sequence_x(query_sequence)
            algn.change_sequence_y(template_sequence)
            algn.set_sequence_x_description("Template")
            algn.set_sequence_y_description("Query")
            write_alignment(algn, 'temp.fasta')

            try:
                a = load_alignment('temp.fasta')
                template_full_path = templates_directory + template_path
                t = load_template(template_full_path)
                m = create_model(t,a)
                m.write_pdb_file('temp.pdb')

                query_full_path = templates_directory + query_path
                rmsd = get_rmsd(query_full_path, 'temp.pdb')
            except:
                rmsd = float("inf")

            print rmsd
            rmsds.append(rmsd)
            i+=1
        print rmsds



main()

