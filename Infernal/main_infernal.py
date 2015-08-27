__author__ = 'rna'

from Infernal import Infernal
from ConfigParser import ConfigParser


def get_config(path):
    config = ConfigParser()
    config.read(path)
    section = 'Infernal'
    options = config.options(section)
    dict1 = dict()
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            dict1[option] = None
    return dict1

def main():
    config = get_config("config.ini")
    inf = Infernal(config)
    families = inf.get_families_for_sequence("GCCGAUAUAGCUCAGUUGGUAGAGCAGCGCAUUCGUAAUGCGAAGGUCGUAGGUUCGACUCCUAUUAUCGGCACCA")
    print families

if __name__ == "__main__":
    main()