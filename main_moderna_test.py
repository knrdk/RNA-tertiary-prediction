__author__ = 'Konrad Kopciuch'

from moderna import *

a = load_alignment('/home/rna/RNA/infernal_align.fa')
t = load_template('/home/rna/RNA/Templates/1QTQ_B.pdb','A')

m = create_model(t,a)

m.write_pdb_file('/home/rna/RNA/infernal_model.pdb')
