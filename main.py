__author__ = 'Konrad Kopciuch'

import sys
import os
from multiprocessing import current_process
from Config import Config
from Repository.MongoTemplateRepository import MongoTemplateRepository
from SVM.templates_ranking import get_templates_ranking
from Utils.Alignment import Alignment, write_alignment
from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
import SCFG.ScoringMatrix as sm
from moderna import load_alignment, load_template, create_model, Sequence


def __get_unmodified_sequence(sequence):
    moderna_seq = Sequence(sequence)
    unmodified = moderna_seq.seq_without_modifications
    return str(unmodified)


def get_alignment(query_sequence, template_unmodified_sequence, template_secondary_structure, template_sequence):
    single_matrix, double_matrix = sm.get_scoring_matrices('config.ini')
    parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)

    query_unmodified_sequence = __get_unmodified_sequence(query_sequence)

    scfg = parser.get_SCFG(template_secondary_structure, template_unmodified_sequence)
    scfg.align(query_unmodified_sequence)
    algn = scfg.get_alignment()
    assert isinstance(algn, Alignment)
    algn.change_template_sequence(template_sequence)
    algn.change_query_sequence(query_sequence)
    return algn


def get_template_path(template_directory, template_id):
    filename = template_id + '.pdb'
    return os.path.join(template_directory, filename)


def try_remove_file(file_path):
    try:
        os.remove(file_path)
    except: return False
    return True


def __get_temp_alignment_file_path():
    process_id = str(current_process().ident)
    return process_id + '_temp_alignment.fasta'


def build_model(template_id, sequence, output_path, template_directory):
    repo = MongoTemplateRepository()
    (template_sequence, template_unmodified_sequence, template_secondary_structure) = repo.get_template_info(template_id)

    temp_alignment_file = __get_temp_alignment_file_path()
    try:
        algn = get_alignment(sequence, template_unmodified_sequence, template_secondary_structure, template_sequence)
        write_alignment(algn, temp_alignment_file)
    except:
        print 'BLAD w trakcie dopasowania sekwencji: ', str(template_id), str(sequence)
        return False

    template_path= get_template_path(template_directory, template_id)

    try:
        a = load_alignment(temp_alignment_file)
        t = load_template(template_path)
        m = create_model(t,a)
        m.write_pdb_file(output_path)
    except:
        print 'BLAD w trakcie budowania modelu: ', str(template_id), str(sequence)
        return False

    try_remove_file(temp_alignment_file)

    return True


def __print_template_ranking(ranking):
    for (template_id, probability) in ranking:
        print template_id, probability


def main_build_model(sequence, svm_file, output_path, template_directory):
    print 'Tworzenie rankingu szablonow'
    try:
        unmodified_sequence = str(Sequence(sequence).seq_without_modifications)
        template_ranking = get_templates_ranking(svm_file, unmodified_sequence)
    except:
        print 'Blad w trakcie tworzenia rankingu szablonow'
        return
    print 'Zakonczono tworzenie rankingu szablonow'

    __print_template_ranking(template_ranking)


    for (template_id, probability) in template_ranking:
        print 'Budowanie modelu za pomoca szablonu: ', template_id
        result = build_model(template_id, sequence, output_path, template_directory)
        if result:
            print 'model zapisany w pliku: ', output_path
            return
        else:
            print 'utworzenie modelu nie powiodlo sie, proba uzycia kolejnego szablonu'
    print 'Brak dostepnych szablonow'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Uzycie: main.py output_file sequence [svm_file]'
    else:
        config = Config('config.ini')

        output_file = sys.argv[1]
        sequence = sys.argv[2]
        if len(sys.argv) == 4:
            svm_file = sys.argv[3]
        else:
            svm_file = config.get_svm_file()
        template_directory = config.get_template_directory()
        main_build_model(sequence, svm_file, output_file, template_directory)

