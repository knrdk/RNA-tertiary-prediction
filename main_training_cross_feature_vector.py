__author__ = 'Konrad Kopciuch'

from os import listdir
from multiprocessing import Pool, cpu_count
from functools import partial
import traceback
from moderna import load_template, load_alignment, create_model

from Config import Config
from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices
from Utils.Alignment import *
from RMSD.RMSD import get_rmsd
import Utils.FloatList as fl
import Utils.ThreadPool as tp
from Training.SequenceProvider import get_sequences
from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator


def process_pair(sinfo):
    (template_path,
     query_path,
     query_sequence,
     query_sequence_without_modifications,
     template_sequence,
     template_sequence_without_modifications,
     template_secondary_structure) = sinfo

    template_id = template_path.split('.')[0]

    fvc = FeatureVectorCalculator()
    vector = fvc.get_feature_vector(query_sequence_without_modifications,
                                    template_id, template_sequence_without_modifications, template_secondary_structure)
    vector_as_str = fl.convert_to_string(vector)
    print query_path, template_path, vector_as_str
    return (query_path, template_path, vector_as_str)




def main_training_cross_feature_vector():
    cfg = Config('config.ini')
    templates_directory = cfg.get_template_directory()
    training_templates_directory = cfg.get_training_set_directory()
    results_file = cfg.get_feature_vectors_path()

    templates_paths = list(listdir(templates_directory))
    training_paths = list(listdir(training_templates_directory))

    print "Liczba szablonow: ", len(templates_paths)
    print "Liczba elementow zbioru treningowego: ", len(training_paths)

    print 'ladowanie danych o sekwencjach'
    templates_sequences = get_sequences(templates_directory, templates_paths)
    training_sequences = get_sequences(training_templates_directory, training_paths)
    print "dane o sekwencjach zaladowane"

    data = list()
    for query_path in training_paths:
            for template_path in templates_paths:
                if query_path == template_path:
                    continue
                (q_seq, q_unm, q_ss) = training_sequences[query_path]
                (t_seq, t_unm, t_ss) = templates_sequences[template_path]
                record = (template_path, query_path, q_seq, q_unm, t_seq, t_unm, t_ss)
                data.append(record)

    #func = partial(process_pair, templates_directory, training_templates_directory)
    pool = tp.get_thread_pool()
    results = pool.map(process_pair, data)

    with open(results_file, 'w') as f:
        for (query_path, template_path, value) in results:
            f.write(query_path + '\t' + template_path + '\t' + str(value) + '\n')
            f.flush()

if __name__ == '__main__':
    main_training_cross_feature_vector()

