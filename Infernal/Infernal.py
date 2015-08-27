__author__ = 'Konrad Kopciuch'

import subprocess
import os

from CmScanOutputParser import CmScanOutputParser


class Infernal:
    def __init__(self, config):
        self.config = config

    def get_families_for_sequence(self, sequence):
        temp_file_path = self.config['tempscanfilepath']
        with open(temp_file_path,'w+') as f:
            f.write(">sequence")
            f.write(sequence)
        output = Infernal.__scan(temp_file_path)
        parser = CmScanOutputParser(output)
        families = parser.get_families_above_threshold()
        Infernal.__delete_file_if_exist(temp_file_path)
        return families

    def __scan(self, input_path):
        cmscan_path = self.config['cmscan']
        cmdatabase_path = self.config['cmdatabase']
        proc = subprocess.Popen([cmscan_path, cmdatabase_path, input_path], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        return output

    @staticmethod
    def __delete_file_if_exist(path):
        try:
            os.remove(path)
        except OSError:
            pass