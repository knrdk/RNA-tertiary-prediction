__author__ = 'Konrad Kopciuch'

from moderna import load_model
from Config import Config
from main import main_build_model
import os

def __get_sequences_from_pdb(path):
    t = load_model(path)
    sequence = str(t.get_sequence())
    t.remove_all_modifications()
    unmodified_sequence = str(t.get_sequence())
    return sequence, unmodified_sequence

def main(config):
    verification_directory = '/home/rna/RNA/VerificationSet'
    verification_results = '/home/rna/RNA/VerificationResult'
    structures = os.listdir(verification_directory)
    for structure in structures:
        full_path = os.path.join(verification_directory, structure)
        sequence, unmodified_sequence = __get_sequences_from_pdb(full_path)

        model_path = 'model_'+structure
        output_path = os.path.join(verification_results, model_path)
        print 'Lancuch: ', structure
        print 'Sekwencja: ', sequence
        print 'Sekwencja bez modyfikacji: ', unmodified_sequence
        try:
            main_build_model(sequence, unmodified_sequence, config.get_svm_file(), output_path, config.get_template_directory())
        except:
            print "ERROR: ", structure


if __name__ == '__main__':
    config = Config('config.ini')
    main(config)

