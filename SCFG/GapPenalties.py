# coding=UTF-8

__author__ = 'Konrad Kopciuch'

from GapClasses import *

def get_penalties_dictionary(a, b):
    """
    Zwraca macierz zawierajaca kary za przerwy w dopasowaniu sekewncji
    :param a: parametr alfa z publikacji "RSEARCH: Finding homologs of single structured RNA sequences" Klein, Eddy
    :param b: parametr beta z tej publikacji
    :return: słownik dwuwymiarowy indeksowany klasami kar za otwarcie. Pierwszy argument From_class, drugi To_class
    """
    return {
        M_cl: {
            M_cl: 0,
            IL_cl: 0.5*a,
            DL_cl: 0.5*a,
            IR_cl: 0.5*a,
            DR_cl: 0.5*a,
            DB_cl: 0.5*a
        },
        IL_cl: {
            M_cl: b + 0.5*a,
            IL_cl: b,
            DL_cl: b+a,
            IR_cl: b+a,
            DR_cl: b+a,
            DB_cl: b+1.5*a
        },
        DL_cl: {
            M_cl: b + 0.5*a,
            IL_cl: b + a,
            DL_cl: b,
            IR_cl: b + a,
            DR_cl: b + a,
            DB_cl: b + 0.5*a
        },
        IR_cl: {
            M_cl: b + 0.5*a,
            DL_cl: b + a,
            IR_cl: b,
            DR_cl: b + a,
            DB_cl: b + 1.5*a
        },
        DR_cl: {
            M_cl: b + 0.5*a,
            IL_cl: b + a,
            DL_cl: b + a,
            IR_cl: b + a,
            DR_cl: b,
            DB_cl: b + 1.5*a
        },
        DB_cl: {
            M_cl: 2*b + a,
            IL_cl: 2*b + 1.5*a,
            DL_cl: 2*b + 0.5*a,
            IR_cl: 2*b + 1.5*a,
            DR_cl: 2*b + 0.5*a,
            DB_cl: 2*b
        }
    }
