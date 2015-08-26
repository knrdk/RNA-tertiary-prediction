__author__ = 'Konrad Kopciuch'

import subprocess

#wrapper for unix executable
class Infernal:
    __cmscan_path = "/home/rna/infernal/cmscan"
    __cmdatabase = "/home/rna/rfam/Rfam.cm"

    def scan(self):
        input_path = "/home/rna/query.fa"
        subprocess.check_call([Infernal.__cmscan_path, Infernal.__cmdatabase, input_path])