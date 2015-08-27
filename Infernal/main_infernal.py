__author__ = 'rna'

from Infernal import Infernal
from FamilyFileParser import FamilyFileParser

def main():
    inf = Infernal()
    families = inf.get_families_for_sequence("GCGUCG")
    print families


if __name__ == "__main__":
    main()