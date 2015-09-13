__author__ = 'rna'

from moderna import load_template
from multiprocessing import Pool, cpu_count
import functools


def __get_thread_pool():
    try:
        cpus = cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return Pool(processes=cpus)


def __load_sequences(templates_directory, template_path):
    '''
    Funkcja za pomoca pakietu moderna odczytuje informacje o sekwencji i strukturze drugorzedowej z pliku pdb
    :param templates_directory: folder z szablonami
    :param template_path: nazwa pliku z szablonem
    :return: (sekwencja, niezmodyfikowana sekwencja, struktura drugorzedowa)
    '''
    full_path = templates_directory + template_path
    tmpl = load_template(full_path)
    sequence = tmpl.get_sequence()
    unmodified_sequence = str(sequence.seq_without_modifications)
    secondary_structure = str(tmpl.get_secstruc())
    return str(sequence), unmodified_sequence, secondary_structure


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
    pool = __get_thread_pool()
    q = pool.map(func, paths)

    output = dict()
    for (index, path) in enumerate(paths):
        output[path] = q[index]
    return output

