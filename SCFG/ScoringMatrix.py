__author__ = 'Konrad Kopciuch'

from ConfigParser import ConfigParser
from RibosumMatrix.RibosumParser import RibosumParser


def __get_ribosum_matrix_path(config_path):
    config = ConfigParser()
    config.read(config_path)
    section = 'Ribosum'
    matrix_path = "matrixpath"
    return config.get(section, matrix_path)


def get_ribosum_matrices():
    ribosum_matrix_path = __get_ribosum_matrix_path("config.ini")
    parser = RibosumParser(ribosum_matrix_path)
    sm = parser.get_single_matrix()
    dm = parser.get_double_matrix()
    return sm, dm