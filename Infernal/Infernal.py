__author__ = 'Konrad Kopciuch'

import subprocess
import os
from multiprocessing import current_process
from CmScanOutputParser import CmScanOutputParser


class Infernal:
    def __init__(self, cmscan_path, cmdatabase_path):
        self.cmscan_path = cmscan_path
        self.cmdatabase_path = cmdatabase_path


    def get_families_for_sequence(self, sequence):
        process = current_process()
        print str(process.name, process.ident)
        temp_file_path = 'temp_infernal_cmscan.fasta'
        with open(temp_file_path,'w') as f:
            f.write(">sequence")
            f.write('\n')
            f.write(sequence)
        output = self.__scan(temp_file_path)
        parser = CmScanOutputParser(output)
        families = parser.get_families_above_threshold()
        Infernal.__delete_file_if_exist(temp_file_path)
        return families

    def __scan(self, input_path):
        cmscan_path = self.cmscan_path
        cmdatabase_path = self.cmdatabase_path
        proc = subprocess.Popen([cmscan_path, cmdatabase_path, input_path], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        return output

    @staticmethod
    def __delete_file_if_exist(path):
        try:
            os.remove(path)
        except OSError:
            pass