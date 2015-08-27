__author__ = 'rna'

from Infernal import Infernal
from FamilyFileParser import FamilyFileParser
from CmScanOutputParser import CmScanOutputParser

def main():
    inf = Infernal()
    output = inf.scan()

    parser = CmScanOutputParser(output)
    families = parser.get_families_above_threshold()
    print families


if __name__ == "__main__":
    main()