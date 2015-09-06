__author__ = 'Konrad Kopciuch'

from Config import Config
from RibosumMatrix.RibosumParser import RibosumParser


def __get_ribosum_matrix_path(config_path):
    config = Config(config_path)
    return config.get_ribosum_matrix_path()

def get_scoring_matrices(config_path):
    ribosum_matrix_path = __get_ribosum_matrix_path(config_path)
    parser = RibosumParser(ribosum_matrix_path)
    sm = parser.get_single_matrix()
    dm = parser.get_double_matrix()
    return sm, dm