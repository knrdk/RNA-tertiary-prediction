__author__ = 'Konrad Kopciuch'

from math import sqrt, pow, erf


def __get_pvalue_general(a, b, chain_length, rmsd):
    std = 1.8
    average = a * pow(chain_length, 0.41) - b
    z = (rmsd - average)/std
    pvalue = (1 + erf(z/sqrt(2)))/2.0
    return pvalue


def __get_pvalue_without_base_pairing(chain_length, rmsd):
    a = 6.4
    b = 12.7
    return __get_pvalue_general(a, b, chain_length, rmsd)


def __get_pvalue_with_base_pairing(chain_length, rmsd):
    a = 5.1
    b = 15.8
    return __get_pvalue_general(a, b, chain_length, rmsd)


def get_pvalue(chain_length, rmsd, base_pairing=True):
    if base_pairing:
        return __get_pvalue_with_base_pairing(chain_length, rmsd)
    else:
        return __get_pvalue_without_base_pairing(chain_length, rmsd)

