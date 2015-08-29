__author__ = 'Konrad Kopciuch'

from moderna import *

a = load_alignment('/home/rna/RNA/align.fa')
t = load_template('/home/rna/RNA/pdb2zue.ent','B') #/home/rna/RNA/Templates/3AM1_B.pdb
clean_structure(t)
m = create_model(t,a)

m.write_pdb_file('/home/rna/RNA/nw_model.pdb')
