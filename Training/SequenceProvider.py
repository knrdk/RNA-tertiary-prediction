__author__ = 'Konrad Kopciuch'

from moderna import load_model
from multiprocessing import Pool, cpu_count
import functools
from Utils.ThreadPool import get_thread_pool


def __load_sequences(templates_directory, template_path):
    '''
    Funkcja za pomoca pakietu moderna odczytuje informacje o sekwencji i strukturze drugorzedowej z pliku pdb
    :param templates_directory: folder z szablonami
    :param template_path: nazwa pliku z szablonem
    :return: (sekwencja, niezmodyfikowana sekwencja, struktura drugorzedowa)
    '''
    full_path = templates_directory + template_path
    tmpl = load_model(full_path)
    sequence = str(tmpl.get_sequence())
    secondary_structure = str(tmpl.get_secstruc())
    tmpl.remove_all_modifications()
    unmodified_sequence = str(tmpl.get_sequence())

    return sequence, unmodified_sequence, secondary_structure


def get_sequences(directory, paths):
    '''
    Funkcja za pomoca programu ModeRNA odczytuje z plikow pdb informacje o sekwencji, niezmodyfikowanej sekwencji
    oraz strukturze drugorzedowej dla podanych plikow i zwraca je jako slownik
    :param directory: Folder w ktorym znajduja sie pliki pdb
    :param paths: lista zawierajaca nazwy plikow pdb
    :return: Slownik ktory dla klucza ktory jest nazwa pliku pdb zwraca trojke:
    sekwencja, niezmodyfikowana sekwencja, struktura drugorzedowa
    '''
    func = functools.partial(__load_sequences, directory)
    pool = get_thread_pool()
    q = pool.map(func, paths)

    output = dict()
    for (index, path) in enumerate(paths):
        output[path] = q[index]
    return output

