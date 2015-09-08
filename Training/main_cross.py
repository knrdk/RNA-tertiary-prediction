__author__ = 'rna'

from os import listdir

from moderna import load_template, load_alignment, create_model

from Config import Config
from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices
from Utils.Alignment import *
from RMSD.RMSD import get_rmsd
from SequenceProvider import SequenceProvider

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

def get_alignment(template_sequence_provider, query_sequence_provider, template_path, query_path):
    query_sequence = query_sequence_provider.get_sequence(query_path)
    query_sequence_without_modifications = query_sequence_provider.get_unmodified_sequence(query_path)
    template_sequence = template_sequence_provider.get_sequence(template_path)
    template_sequence_without_modifications = template_sequence_provider.get_unmodified_sequence(template_path)
    template_secondary_structure = template_sequence_provider.get_secondary_structure(template_path)

    #algn = __scfg_align(template_secondary_structure, template_sequence_without_modifications, query_sequence_without_modifications)
    algn = __nw_align(template_sequence_without_modifications, query_sequence_without_modifications)

    algn.change_template_sequence(template_sequence)
    algn.change_query_sequence(query_sequence)
    algn.set_template_description("Template")
    algn.set_query_description("Query")
    return algn

def main():
    cfg = Config('config.ini')
    templates_directory = cfg.get_template_directory()
    training_templates_directory = cfg.get_training_set_directory()
    training_results_file = cfg.get_training_results_path()
    templates_sequence_provider = SequenceProvider(templates_directory)
    training_sequence_provider = SequenceProvider(training_templates_directory)

    templates_paths = list(listdir(templates_directory))
    training_paths = list(listdir(training_templates_directory))

    print "Liczba szablonow: ", len(templates_paths)
    print "Liczba elementow zbioru treningowego: ", len(training_paths)
    print "Liczba par: ", str(len(templates_paths)*len(training_paths))

    i = 1
    with open(training_results_file, 'w') as f:
        for query_path in training_paths:
            for template_path in templates_paths:
                if query_path == template_path:
                    continue
                print i
                print query_path, template_path

                algn = get_alignment(templates_sequence_provider, training_sequence_provider, template_path, query_path)
                write_alignment(algn, 'temp.fasta')

                try:
                    a = load_alignment('temp.fasta')
                    template_full_path = templates_directory + template_path
                    t = load_template(template_full_path)
                    m = create_model(t,a)
                    m.write_pdb_file('temp.pdb')

                    query_full_path = training_templates_directory + query_path
                    rmsd = get_rmsd(query_full_path, 'temp.pdb')
                except:
                    rmsd = float("inf")

                print rmsd
                i+=1
                f.write(query_path + '\t' + template_path + '\t' + str(rmsd) + '\n')
                f.flush()


main()

