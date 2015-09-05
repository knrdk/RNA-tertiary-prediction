__author__ = 'Konrad Kopciuch'

from Config import Config
from RibosumMatrix.RibosumParser import RibosumParser


def __get_ribosum_matrix_path(config_path):
    config = Config('./../config.ini')
    return config.get_ribosum_matrix_path()

def get_scoring_matrices():
    ribosum_matrix_path = __get_ribosum_matrix_path("config.ini")
    parser = RibosumParser(ribosum_matrix_path)
    sm = parser.get_single_matrix()
    dm = parser.get_double_matrix()
    return sm, dm