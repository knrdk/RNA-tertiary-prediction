__author__ = 'rna'

from os import listdir

from moderna import load_template, load_alignment, create_model

from Config import Config
from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices
from Utils.Alignment import *
from RMSD.RMSD import get_rmsd


class SequenceProvider:

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

def __nw_align(template_sequence, query_sequence):
    nw = NeedlemanWunsch(template_sequence, query_sequence)
    nw.align()
    return nw.get_alignment()

def __scfg_align(template_secstruct, template_sequence, query_sequence):
    single_matrix, double_matrix = get_scoring_matrices('config.ini')
    parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
    scfg = parser.get_SCFG(template_secstruct, template_sequence)
    scfg.align(query_sequence)
    algn = scfg.get_alignment()
    return algn

def get_alignment(sequence_provider, template_path, query_path):
    query_sequence = sequence_provider.get_sequence(query_path)
    query_sequence_without_modifications = sequence_provider.get_unmodified_sequence(query_path)
    template_sequence = sequence_provider.get_sequence(template_path)
    template_sequence_without_modifications = sequence_provider.get_unmodified_sequence(template_path)
    template_secondary_structure = sequence_provider.get_secondary_structure(template_path)

    algn = __scfg_align(template_secondary_structure, template_sequence_without_modifications, query_sequence_without_modifications)

    algn.change_template_sequence(template_sequence)
    algn.change_query_sequence(query_sequence)
    algn.set_template_description("Template")
    algn.set_query_description("Query")
    return algn

def main():
    cfg = Config('config.ini')
    templates_directory = cfg.get_template_directory()
    training_templates_directory = cfg.get_training_templates_directory()
    training_results_file = cfg.get_training_results_path()
    sequence_provider = SequenceProvider(templates_directory)

    templates_paths = list(listdir(templates_directory))
    training_paths = list(listdir(training_templates_directory))
    i = 1
    with open(training_results_file, 'w') as f:
        for query_path in training_paths:
            for template_path in templates_paths:
                if query_path == template_path:
                    continue
                print i
                print query_path, template_path

                algn = get_alignment(sequence_provider, template_path, query_path)
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
                i+=1
                f.write(query_path + '\t' + template_path + '\t' + str(rmsd))
                f.flush()


main()

