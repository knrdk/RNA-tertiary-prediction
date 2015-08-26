__author__ = 'Konrad Kopciuch'

import subprocess

#wrapper for unix executable
class Infernal:
    __cmscan_path = "/home/rna/infernal/cmscan"
    __cmdatabase = "/home/rna/rfam/Rfam.cm"


    def __init__(self):
        pass

    def scan(self):
        input_path = "/home/rna/query/subject.fa"
        proc = subprocess.Popen([Infernal.__cmscan_path, Infernal.__cmdatabase, input_path], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        print output