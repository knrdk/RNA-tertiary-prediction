__author__ = 'Konrad Kopciuch'

from moderna import load_template
from Config import Config
from main import main_build_model
import os

def main():
    verification_directory = '/home/rna/RNA/VerificationSet'
    structures = os.listdir(verification_directory)
    for structure in structures:
        full_path = os.path.join(verification_directory, structure)
        t = load_template(full_path)
        sequence = t.get_sequence()
        print structure, sequence




if __name__ == '__main__':
    config = Config('config.ini')
    main()

