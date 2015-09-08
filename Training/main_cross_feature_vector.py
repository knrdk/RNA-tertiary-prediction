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
from PairwiseSimilarity.FeatureVectorCalculator import FeatureVectorCalculator

def __numbers_list_as_string(list):
    length = len(list)
    s = ''
    for i in range(length):
        s += str(list[i])
        if i < length-1:
            s += ';'
    return s

def main():
    cfg = Config('./../config.ini')
    templates_directory = cfg.get_template_directory()
    training_templates_directory = cfg.get_training_set_directory()
    feature_vectors_file = cfg.get_feature_vectors_path()
    templates_sequence_provider = SequenceProvider(templates_directory)
    training_sequence_provider = SequenceProvider(training_templates_directory)

    templates_paths = list(listdir(templates_directory))
    training_paths = list(listdir(training_templates_directory))

    print "Liczba szablonow: ", len(templates_paths)
    print "Liczba elementow zbioru treningowego: ", len(training_paths)
    print "Liczba par: ", str(len(templates_paths)*len(training_paths))

    i = 1
    with open(feature_vectors_file, 'w') as f:
        for query_path in training_paths:
            for template_path in templates_paths:
                if query_path == template_path:
                    continue
                print i
                print query_path, template_path

                template_sequence = templates_sequence_provider.get_unmodified_sequence(template_path)
                template_secondary_structure = templates_sequence_provider.get_secondary_structure(template_path)
                query_sequence = training_sequence_provider.get_unmodified_sequence(query_path)

                template_id = template_path.split('.')[0]
                print template_id

                fvc = FeatureVectorCalculator()
                vector = fvc.get_feature_vector(query_sequence, template_id, template_sequence, template_secondary_structure)
                print vector


                i+=1
                f.write(query_path + '\t' + template_path + '\t' + __numbers_list_as_string(vector) + '\n')
                f.flush()

if __name__ == '__main__':
    main()

