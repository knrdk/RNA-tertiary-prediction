__author__ = 'Konrad Kopciuch'

from moderna import load_model
from Config import Config
from main import main_build_model
import os

def main(config):
    verification_directory = '/home/rna/RNA/VerificationSet'
    verification_results = '/home/rna/RNA/VerificationResult'
    structures = os.listdir(verification_directory)
    for structure in structures:
        full_path = os.path.join(verification_directory, structure)

        t = load_model(full_path)
        sequence = str(t.get_sequence())
        t.remove_all_modifications()
        unmodified_sequence = str(t.get_sequence())
        model_path = 'model_'+structure
        output_path = os.path.join(verification_results, model_path)
        print structure
        print sequence
        print unmodified_sequence
        try:
            main_build_model(sequence, config.get_svm_file(), output_path, config.get_template_directory())
        except:
            print "ERROR: ", structure




if __name__ == '__main__':
    config = Config('config.ini')
    main(config)

