__author__ = 'Konrad Kopciuch'

import subprocess
import os

from CmScanOutputParser import CmScanOutputParser

#wrapper for unix executable
class Infernal:
    __cmscan_path = "/home/rna/infernal/cmscan"
    __cmdatabase = "/home/rna/rfam/Rfam.cm"
    __tmp_file_path = "/home/rna/RNA/temp_get_families_for_sequence.fa"

    def __init__(self):
        #TODO: read configuration
        pass

    def get_families_for_sequence(self, sequence):
        with open(Infernal.__tmp_file_path,'w+') as f:
            f.write(">sequence")
            f.write(sequence)
        output = Infernal.__scan(Infernal.__tmp_file_path)
        parser = CmScanOutputParser(output)
        families = parser.get_families_above_threshold()
        Infernal.__delete_file_if_exist(sequence)
        return families

    @staticmethod
    def __scan(input_path):
        proc = subprocess.Popen([Infernal.__cmscan_path, Infernal.__cmdatabase, input_path], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        return output

    @staticmethod
    def __delete_file_if_exist(path):
        try:
            os.remove(path)
        except OSError:
            pass