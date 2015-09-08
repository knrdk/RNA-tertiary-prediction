__author__ = 'rna'

from math import sqrt, pow, erf

def __get_pvalue_without_base_pairing(chain_length, rmsd):
    std = 1.8
    a = 4.6 * sqrt(2.0)
    b = 9.1 * sqrt(2.0)
    average = a * pow(chain_length, 0.41) - b
    z = (rmsd - average)/std
    pvalue = (1 + erf(z/sqrt(2)))/2.0
    return pvalue

def __get_pvalue_with_base_pairing(chain_length, rmsd):
    std = 1.8
    a = 3.6 * sqrt(2.0)
    b = 11.2 * sqrt(2.0)
    average = a * pow(chain_length, 0.41) - b
    z = (rmsd - average)/std
    pvalue = (1 + erf(z/sqrt(2)))/2.0
    return pvalue

def get_pvalue(chain_length, rmsd, base_pairing=True):
    if base_pairing:
        return __get_pvalue_with_base_pairing(chain_length, rmsd)
    else:
        return __get_pvalue_without_base_pairing(chain_length, rmsd)

