__author__ = 'Konrad Kopciuch'

import multiprocessing as mp

def get_thread_pool():
    try:
        cpus = mp.cpu_count()
    except NotImplementedError:
        cpus = 1   # arbitrary default

    return mp.Pool(processes=cpus)

