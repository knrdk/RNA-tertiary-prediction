__author__ = 'rna'

from os import listdir

from moderna import load_template, load_alignment, create_model

from Config import Config
from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices
from Utils.Alignment import *
from RMSD.RMSD import get_rmsd
from os import remove
from multiprocessing import Pool, cpu_count
from functools import partial


def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)

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

def get_alignment(template_path,
                  query_path,
                  query_sequence,
                  query_sequence_without_modifications,
                  template_sequence,
                  template_sequence_without_modifications,
                  template_secondary_structure):

    algn = __scfg_align(template_secondary_structure, template_sequence_without_modifications, query_sequence_without_modifications)

    algn.change_template_sequence(template_sequence)
    algn.change_query_sequence(query_sequence)
    algn.set_template_description("Template")
    algn.set_query_description("Query")
    return algn

def process_pair(templates_directory,
                 training_templates_directory,
                  sinfo):
    (template_path,
     query_path,
     query_sequence,
     query_sequence_without_modifications,
     template_sequence,
     template_sequence_without_modifications,
     template_secondary_structure) = sinfo
    algn = get_alignment(template_path, query_path, query_sequence, query_sequence_without_modifications, template_sequence,
                         template_sequence_without_modifications, template_secondary_structure)
    tmp_filename = query_path.split('.')[0] + template_path.split('.')[0]
    write_alignment(algn, tmp_filename + '.fasta')
    try:
        a = load_alignment(tmp_filename + '.fasta')
        template_full_path = templates_directory + template_path
        t = load_template(template_full_path)
        m = create_model(t,a)
        m.write_pdb_file(tmp_filename + '.pdb')

        query_full_path = training_templates_directory + query_path
        rmsd = get_rmsd(query_full_path, tmp_filename + '.pdb')
    except:
        rmsd = float("inf")

    try:
        remove(tmp_filename + '.fasta')
        remove(tmp_filename + '.pdb')
    except:
        pass

    print query_path, template_path, rmsd
    return (query_path, template_path, rmsd)

def load_sequences(templates_directory, template_path):
    full_path = templates_directory + template_path
    tmpl = load_template(full_path)
    sequence = tmpl.get_sequence()
    unmodified_sequence = str(sequence.seq_without_modifications)
    secondary_structure = str(tmpl.get_secstruc())
    return str(sequence), unmodified_sequence, secondary_structure

def get_sequences(directory, paths):
    func = partial(load_sequences, directory)
    pool = __get_thread_pool()
    q = pool.map(func, paths)

    output = dict()
    for (index, path) in enumerate(paths):
        output[path] = q[index]
    return output

def main():
    cfg = Config('config.ini')
    templates_directory = cfg.get_template_directory()
    training_templates_directory = cfg.get_training_set_directory()
    training_results_file = cfg.get_training_results_path()

    templates_paths = list(listdir(templates_directory))
    training_paths = list(listdir(training_templates_directory))

    print "Liczba szablonow: ", len(templates_paths)
    print "Liczba elementow zbioru treningowego: ", len(training_paths)

    templates_sequences = get_sequences(templates_directory, templates_paths)
    training_sequences = get_sequences(training_templates_directory, training_paths)

    print "dane o sekwencji zaladowane"

    data = list()
    for query_path in training_paths:
            for template_path in templates_paths:
                if query_path == template_path:
                    continue
                (q_seq, q_unm, q_ss) = training_sequences[query_path]
                (t_seq, t_unm, t_ss) = templates_sequences[template_path]
                record = (template_path, query_path, q_seq, q_unm, t_seq, t_unm, t_ss)
            data.append(record)

    func = partial(process_pair, templates_directory, training_templates_directory)
    pool = __get_thread_pool()
    results = pool.map(func, data)

    with open(training_results_file, 'w') as f:
        for (query_path, template_path, rmsd) in results:
            f.write(query_path + '\t' + template_path + '\t' + str(rmsd) + '\n')
            f.flush()


if __name__ == '__main__':
    main()

